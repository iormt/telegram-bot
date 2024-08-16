import requests
from api_requests_module.open_ai_request import OpenAIRequest
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext
from counter_module import counter
import os



### Base Command ###
class Command(ABC):
    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext) -> None:
        pass


### Concrete Commands ###
class WeatherCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):

        city = "Montevideo"  # You can modify this to get the city from user input
        api_key = os.getenv('OPEN_WEATHER_MAP_API_KEY')
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        
        response = requests.get(url)
        if response.status_code != 200:
            await self.handle_error_response(update, context, url, response)
            return
        await self.handle_success_response(update, context, city, response)


    async def handle_success_response(self, update, context, city, response):
        data = response.json()
        message = self.create_message(city, data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


    def create_message(self, city, data):
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']

        message = f"El clima en {city} es {weather_description} con una temperatura de {temperature}°C. "
        message += '\n\n' + self.get_open_ai_tips(message)
        return message


    def get_open_ai_tips(self, message):
        request_text = f"Dado el siguiente mensaje:\n\n{message}\n\n Dar una recomendacion segun la descripcion el clima y ofrecer consejos adicionales o información interesante sobre la ciudad. Se breve"
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_request(request_text)

        # Extract the sentiment analysis result
        tips_and_information: str = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                tips_and_information += chunk.choices[0].delta.content
        return tips_and_information


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


class SentimentAnalysisCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):
        
        # Collect the conversation history
        chat_id = update.effective_chat.id
        messages = context.bot_data.get(chat_id, [])
        
        # Prepare the conversation text
        conversation_text = "\n".join(messages)

        # Prepare request text 
        request_text = 'Analiza el sentimiento de la siguiente conversacion y clasificala como positivo, negativo o neutral. Provee una breve explicacion:'
        request_text += f'\n\n{conversation_text}'
        # Send the conversation to OpenAI for sentiment analysis
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_request(request_text)

        # Extract the sentiment analysis result
        sentiment_analysis: str = ''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                sentiment_analysis += chunk.choices[0].delta.content
        

        # Send the result back to the user
        await context.bot.send_message(chat_id=chat_id, text=sentiment_analysis)

