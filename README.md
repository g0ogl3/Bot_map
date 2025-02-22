# Картографический бот Telegram

Этот проект представляет из себя Telegram бота, который взаимодействует с пользователями, позволяя отображать города на карте и управлять списком городов пользователя.

## Основные возможности

- Показать город на карте
- Запомнить город для пользователя
- Показать все запомненные города для пользователя
- Установить цвет маркера для городов
- Нарисовать расстояние между двумя городами
- Показать города из конкретной страны
- Показать города по плотности населения
- Показать города по стране и плотности населения
- Получить информацию о погоде в городе
- Получить текущее время в городе

## Технологии

- **Python 3**: Язык программирования.
- **SQLite**: База данных для хранения информации о пользователях и городах.
- **Matplotlib, Cartopy и Geopy**: Библиотеки для создания графического представления данных.
- **Telebot**: Библиотека для создания и управления Telegram ботами.

### Предварительные требования

- Python 3.7+
- Токен API Telegram-бота
- Ключ API для OpenWeatherMap (для информации о погоде)
- Ключ API для TimeZoneDB (для информации о времени)

## Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/g0ogl3/Bot_map.git
cd Bot_map
```
2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```
3. **Настройте переменные окружения:**

Откройте файл config.py в корневом каталоге проекта и укажите в нем необходимые переменные:
```bash
TOKEN=<your_telegram_bot_token>
WEATHER_API_KEY =<your_API_key_openweathermap>
TIME_API_KEY = <your_API_key_timezonedb>
```
4. **Запуск бота:**
```bash
python bot.py
```

## Использование

- `/start` - Начать взаимодействие с ботом
- `/help` - Показать список доступных команд
- `/show_city <город>` - Показать город на карте
- `/remember_city <город>` - Запомнить город для пользователя
- `/show_my_cities` - Показать все запомненные города для пользователя
- `/set_marker_color <цвет>` - Установить цвет маркера для городов
- `/draw_distance <город1> <город2>` - Показать расстояние между двумя городами
- `/show_cities_by_country <страна>` - Показать города из конкретной страны
- `/show_cities_by_density <мин_плотность> <макс_плотность>` - Показать города по плотности населения
- `/show_cities_by_country_and_density <страна> <мин_плотность> <макс_плотность>` - Показать города по стране и плотности населения
- `/get_weather <город>` - Получить информацию о погоде в городе
- `/get_time <город>` - Получить текущее время в городе


### Пример

Вот пример того, как использовать бота:

1. Запустите бота и получите список доступных команд:
    ```
    /start
    /help
    ```

2. Показать город на карте:
    ```
    /show_city London
    ```

3. Запомнить город для пользователя:
    ```
    /remember_city Paris
    ```

4. Показать все запомненные города для пользователя:
    ```
    /show_my_cities
    ```

5. Установить цвет маркера для городов:
    ```
    /set_marker_color blue
    ```

6. Нарисовать расстояние между двумя городами:
    ```
    /draw_distance London Paris
    ```

7. Показать города из конкретной страны:
    ```
    /show_cities_by_country France
    ```

8. Показать города по плотности населения:
    ```
    /show_cities_by_density 1000 5000
    ```

9. Показать города по стране и плотности населения:
    ```
    /show_cities_by_country_and_density France 1000 5000
    ```

10. Получить информацию о погоде в городе:
    ```
    /get_weather London
    ```

11. Получить текущее время в городе:
    ```
    /get_time London
    ```

