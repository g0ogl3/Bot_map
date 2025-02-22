import sqlite3
from config import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.distance import geodesic
import requests

class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.execute('''CREATE TABLE IF NOT EXISTS user_colors (
                                user_id INTEGER PRIMARY KEY,
                                color TEXT
                            )''')
            conn.commit()

    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_graph(self, path, cities, marker_color='red'):
        fig = plt.figure(figsize=(10, 5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND, facecolor='lightgreen')
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAKES, facecolor='blue')
        ax.add_feature(cfeature.RIVERS)
        ax.add_feature(cfeature.STATES, linestyle='--')
        ax.add_feature(cfeature.RIVERS, edgecolor='blue')
        ax.add_feature(cfeature.LAKES, edgecolor='blue', facecolor='none')
        ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='none')
        ax.add_feature(cfeature.OCEAN, edgecolor='black', facecolor='none')

        for city in cities:
            coordinates = self.get_coordinates(city)
            if coordinates:
                lat, lng = coordinates
                ax.plot(lng, lat, marker='o', color=marker_color, markersize=5, transform=ccrs.Geodetic())
                ax.text(lng + 3, lat - 3, city, transform=ccrs.Geodetic())

        plt.savefig(path)
        plt.close()

    def set_marker_color(self, user_id, color):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('INSERT OR REPLACE INTO user_colors (user_id, color) VALUES (?, ?)', (user_id, color))
            conn.commit()

    def get_marker_color(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT color FROM user_colors WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 'red'

    def draw_distance(self, city1, city2, path):
        coordinates1 = self.get_coordinates(city1)
        coordinates2 = self.get_coordinates(city2)
        if coordinates1 and coordinates2:
            lat1, lng1 = coordinates1
            lat2, lng2 = coordinates2
            distance = geodesic((lat1, lng1), (lat2, lng2)).kilometers

            fig = plt.figure(figsize=(10, 5))
            ax = plt.axes(projection=ccrs.PlateCarree())
            ax.add_feature(cfeature.LAND, facecolor='lightgreen')
            ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
            ax.add_feature(cfeature.COASTLINE, edgecolor='black')
            ax.add_feature(cfeature.BORDERS, linestyle=':')
            ax.add_feature(cfeature.LAKES, facecolor='blue')
            ax.add_feature(cfeature.RIVERS)
            ax.add_feature(cfeature.STATES, linestyle='--')
            ax.add_feature(cfeature.RIVERS, edgecolor='blue')
            ax.add_feature(cfeature.LAKES, edgecolor='blue', facecolor='none')
            ax.add_feature(cfeature.LAND, edgecolor='gray', facecolor='none')
            ax.add_feature(cfeature.OCEAN, edgecolor='gray', facecolor='none')

            ax.plot([lng1, lng2], [lat1, lat2], color='black', linewidth=2, transform=ccrs.Geodetic())
            mid_lat = (lat1 + lat2) / 2 + 5
            mid_lng = (lng1 + lng2) / 2
            ax.text(mid_lng, mid_lat, f'{distance:.2f} km', transform=ccrs.Geodetic(), fontsize=12, ha='center', va='bottom', color='black')

            plt.savefig(path)
            plt.close()

    def get_cities_by_country(self, country):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT city 
                            FROM cities  
                            WHERE country = ?''', (country,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_cities_by_population_density(self, min_density, max_density):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT city 
                            FROM cities  
                            WHERE population_density BETWEEN ? AND ?''', (min_density, max_density))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_cities_by_country_and_density(self, country, min_density, max_density):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT city 
                            FROM cities  
                            WHERE country = ? AND population_density BETWEEN ? AND ?''', (country, min_density, max_density))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_weather(self, city_name):
        api_key = 'YOUR_API_WEATHER_KEY'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f'Weather: {weather}, Temperature: {temperature}°C'
        else:
            return 'Weather information not available'

    def get_time(self, city_name):
        api_key = 'YOUR_API_TIME_KEY'
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=zone&zone={city_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            datetime = data['datetime']
            return f'Current time: {datetime}'
        else:
            return 'Time information not available'

if __name__ == "__main__":
    m = DB_Map(DATABASE)
    m.create_user_table()
