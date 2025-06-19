import requests
from datetime import datetime

def get_weather_forecast(city, target_date, api_key):
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'
    geo_resp = requests.get(geo_url).json()
    if not geo_resp:
        return None

    lat = geo_resp[0]['lat']
    lon = geo_resp[0]['lon']

    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=ru&appid={api_key}'
    forecast_resp = requests.get(forecast_url).json()

    if forecast_resp.get('cod') != '200':
        return None

    target_dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0)
    closest_forecast = None
    min_diff = None

    for item in forecast_resp['list']:
        forecast_time = datetime.fromtimestamp(item['dt'])
        diff = abs((forecast_time - target_dt).total_seconds())
        if min_diff is None or diff < min_diff:
            min_diff = diff
            closest_forecast = item

    if closest_forecast is None:
        return None

    weather = closest_forecast['weather'][0]
    main = closest_forecast['main']
    wind = closest_forecast['wind']

    return {
        'temp': round(main['temp']),
        'feels_like': round(main['feels_like']),
        'description': weather['description'].capitalize(),
        'wind_speed': wind['speed']
    }
