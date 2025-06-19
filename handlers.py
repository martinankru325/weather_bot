from telebot import types
from datetime import datetime, timedelta
from database import History
from weather_api import get_weather_forecast
from config import OPENWEATHER_API_KEY

user_data = {}

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 'Привет! Введите, пожалуйста, название города для прогноза погоды.')

    @bot.message_handler(commands=['help'])
    def send_help(message):
        help_text = (
            "Доступные команды:\n"
            "/start - начать работу с ботом\n"
            "/history - показать список городов, для которых вы запрашивали погоду\n"
            "/help - показать это сообщение"
        )
        bot.send_message(message.chat.id, help_text)

    @bot.message_handler(commands=['history'])
    def send_history(message):
        chat_id = message.chat.id
        query = (History
                 .select(History.city)
                 .where(History.chat_id == chat_id)
                 .distinct())

        cities = [record.city for record in query]

        if not cities:
            bot.send_message(chat_id, "История запросов пуста. Вы ещё не узнавали погоду.")
        else:
            city_list = '\n'.join(f'• {city}' for city in cities)
            bot.send_message(chat_id, f"Вы узнавали погоду для следующих городов:\n{city_list}")

    @bot.message_handler(func=lambda message: True)
    def get_city(message):
        city = message.text.strip()
        user_data[message.chat.id] = {'city': city}

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_today = types.InlineKeyboardButton('Сегодня', callback_data='day_today')
        btn_tomorrow = types.InlineKeyboardButton('Завтра', callback_data='day_tomorrow')
        markup.add(btn_today, btn_tomorrow)

        bot.send_message(message.chat.id, f'Вы выбрали город: {city}. Выберите день для прогноза:', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
    def callback_day(call):
        chat_id = call.message.chat.id

        if chat_id not in user_data or 'city' not in user_data[chat_id]:
            bot.answer_callback_query(call.id, "Сначала введите город командой /start")
            return

        city = user_data[chat_id]['city']
        day_choice = call.data.split('_')[1]

        if day_choice == 'today':
            target_date = datetime.now()
            day_text = 'Сегодня'
        else:
            target_date = datetime.now() + timedelta(days=1)
            day_text = 'Завтра'

        weather_info = get_weather_forecast(city, target_date, OPENWEATHER_API_KEY)

        if weather_info is None:
            bot.answer_callback_query(call.id, "Не удалось получить данные о погоде. Проверьте название города.")
            return

        temp = weather_info['temp']
        feels_like = weather_info['feels_like']
        desc = weather_info['description']
        wind_speed = weather_info['wind_speed']

        History.create(
            chat_id=chat_id,
            city=city,
            day=day_text,
            temp=temp,
            feels_like=feels_like,
            description=desc,
            wind_speed=wind_speed
        )

        msg = (f'Погода в городе {city} на {day_text} ({target_date.strftime("%d.%m.%Y")}):\n'
               f'Температура: {temp}°C\n'
               f'Ощущается как: {feels_like}°C\n'
               f'Описание: {desc}\n'
               f'Скорость ветра: {wind_speed} м/с\n\n'
               'Чтобы узнать погоду для другого города, введите название нового города.')

        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, msg)
