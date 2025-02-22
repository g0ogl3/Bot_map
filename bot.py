import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                                      "/start - Начать работу с ботом\n"
                                      "/help - Список команд\n"
                                      "/show_city <город> - Показать город на карте\n"
                                      "/remember_city <город> - Запомнить город\n"
                                      "/show_my_cities - Показать все запомненные города\n"
                                      "/set_marker_color <цвет> - Установить цвет маркера\n"
                                      "/draw_distance <город1> <город2> - Показать расстояние между двумя городами\n"
                                      "/show_cities_by_country <страна> - Показать города из конкретной страны\n"
                                      "/show_cities_by_density <мин_плотность> <макс_плотность> - Показать города по плотности населения\n"
                                      "/show_cities_by_country_and_density <страна> <мин_плотность> <макс_плотность> - Показать города по плотности и по стране\n"
                                      "/get_weather <город> - Показать погоду в городе\n"
                                      "/get_time <город> - Показать время в городе")

@bot.message_handler(commands=['set_marker_color'])
def handle_set_marker_color(message):
    user_id = message.chat.id
    color = message.text.split()[-1]
    manager.set_marker_color(user_id, color)
    bot.send_message(user_id, f'Цвет маркера установлен на {color}')

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    user_id = message.chat.id
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название города.')
        return
    city_name = parts[1]
    marker_color = manager.get_marker_color(user_id)
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        path = f"{city_name}.png"
        manager.create_graph(path, [city_name], marker_color)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название города.')
        return
    city_name = parts[1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    user_id = message.chat.id
    marker_color = manager.get_marker_color(user_id)
    cities = manager.select_cities(user_id)
    if cities:
        path = "my_cities.png"
        manager.create_graph(path, cities, marker_color)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'У вас нет сохраненных городов.')

@bot.message_handler(commands=['draw_distance'])
def handle_draw_distance(message):
    parts = message.text.split()
    if len(parts) < 3:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите два города.')
        return
    city1 = parts[1]
    city2 = parts[2]
    path = f"{city1}_to_{city2}.png"
    manager.draw_distance(city1, city2, path)
    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['show_cities_by_country'])
def handle_show_cities_by_country(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название страны.')
        return
    country = parts[1]
    cities = manager.get_cities_by_country(country)
    if cities:
        path = f"{country}_cities.png"
        manager.create_graph(path, cities)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'В этой стране нет известных городов.')

@bot.message_handler(commands=['show_cities_by_density'])
def handle_show_cities_by_density(message):
    parts = message.text.split()
    if len(parts) < 3:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите минимальную и максимальную плотность населения.')
        return
    min_density = float(parts[1])
    max_density = float(parts[2])
    cities = manager.get_cities_by_population_density(min_density, max_density)
    if cities:
        path = f"cities_by_density_{min_density}_{max_density}.png"
        manager.create_graph(path, cities)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Нет городов с такой плотностью населения.')

@bot.message_handler(commands=['show_cities_by_country_and_density'])
def handle_show_cities_by_country_and_density(message):
    parts = message.text.split()
    if len(parts) < 4:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название страны, минимальную и максимальную плотность населения.')
        return
    country = parts[1]
    min_density = float(parts[2])
    max_density = float(parts[3])
    cities = manager.get_cities_by_country_and_density(country, min_density, max_density)
    if cities:
        path = f"{country}_cities_by_density_{min_density}_{max_density}.png"
        manager.create_graph(path, cities)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Нет городов в этой стране с такой плотностью населения.')

@bot.message_handler(commands=['get_weather'])
def handle_get_weather(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название города.')
        return
    city_name = parts[1]
    weather_info = manager.get_weather(city_name)
    bot.send_message(message.chat.id, weather_info)

@bot.message_handler(commands=['get_time'])
def handle_get_time(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите название города.')
        return
    city_name = parts[1]
    time_info = manager.get_time(city_name)
    bot.send_message(message.chat.id, time_info)

if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
