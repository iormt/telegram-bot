import os
import requests
from ratelimit import limits, sleep_and_retry


class OpenWeatherMapRequest:
    def __init__(self):
        self.api_key = os.getenv('OPEN_WEATHER_MAP_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set the OPEN_WEATHER_MAP_API_KEY environment variable.")

    @sleep_and_retry
    @limits(calls=5, period=60)


    def make_request(self, city):
        try:
            api_key = os.getenv('OPEN_WEATHER_MAP_API_KEY')
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
            response = requests.get(url)
            return response
        except Exception as e:
            print(f'Error making API request: {e}')
            return None