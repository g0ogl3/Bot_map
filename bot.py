import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)
user_marker_colors = {}

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
                                      "/set_marker_color <цвет> - Установить цвет маркера, если он не будет установлен тогда цвет маркера будет красным")


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    parts = message.text.split()
    user_id = message.chat.id
    city_name = parts[1]
    marker_color = user_marker_colors[user_id] if user_id in user_marker_colors else 'red'
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        path = f"{city_name}.png"
        manager.create_graph(path, [city_name], marker_color)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['set_marker_color'])
def handle_set_marker_color(message):
    user_id = message.chat.id
    color = message.text.split()[-1]
    user_marker_colors[user_id] = color
    bot.send_message(user_id, f'Цвет маркера установлен на {color}')


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    parts = message.text.split()
    marker_color = parts[1] if len(parts) > 1 else 'red'
    cities = manager.select_cities(message.chat.id)
    if cities:
        path = "my_cities.png"
        manager.create_graph(path, cities, marker_color)
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'У вас нет сохраненных городов.')


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
