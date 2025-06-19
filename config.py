import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
OPENWEATHER_API_KEY = os.getenv('OWM_TOKEN')

if not TELEGRAM_TOKEN or not OPENWEATHER_API_KEY:
    raise ValueError("Отсутствует TELEGRAM_TOKEN или OPENWEATHER_API_KEY. Проверьте файл .env")
