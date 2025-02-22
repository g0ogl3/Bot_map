import sqlite3
from config import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import cartopy.crs as ccrs
import cartopy.feature as cfeature



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
            conn.commit()

    def add_city(self,user_id, city_name ):
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

        
    def draw_distance(self, city1, city2):
        pass


if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()
