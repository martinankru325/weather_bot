import telebot
from config import TELEGRAM_TOKEN
from database import initialize_db
from handlers import register_handlers

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():
    initialize_db()
    register_handlers(bot)
    print('Бот запущен...')
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
