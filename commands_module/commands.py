import requests
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext
from constants import constants
from counter_module import counter



### Base Command ###
class Command(ABC):
    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext) -> None:
        pass


### Concrete Commands ###
class WeatherCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):
        city = "Montevideo"  # You can modify this to get the city from user input
        api_key = constants.OPEN_WEATHER_MAP_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        
        response = requests.get(url)
        if response.status_code != 200:
            await self.handle_error_response(update, context, url, response)
            return
        await self.handle_success_response(update, context, city, response)


    async def handle_success_response(self, update, context, city, response):
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        message = f"El clima en {city} es {weather_description} con una temperatura de {temperature}°C."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    async def handle_error_response(self, update, context, url, response):
        message = "No se pudo obtener la información del clima. Por favor, intenta de nuevo más tarde."
        print(f'Weather request returned status code: {response.status_code}. Problem is {response.reason}')
        print(f'URL: {url}')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


class CounterCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):
        user_id = str(update.message.from_user.id)
        self.increment_counter(user_id)
        message = f"Contador: {counter.counter_data[user_id]}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)



    def increment_counter(self, user_id : str):
        if user_id not in counter.counter_data:
            counter.counter_data[user_id] = 0

        new_counter_value = counter.counter_data[user_id] + 1
        counter.counter_data[user_id] = new_counter_value
        counter.save_counter_data()