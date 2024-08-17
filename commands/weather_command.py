from commands.base_command import Command 
from telegram.ext import CallbackContext
from telegram import Update
from api_requests.open_ai_request import OpenAIRequest
from api_requests.weather_request import OpenWeatherMapRequest
from localizations import localization_handler
from config import constants


class WeatherCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):

        city = constants.CITY_NAME  # You can modify this to get the city from user input
        weather_requests = OpenWeatherMapRequest()
        response = weather_requests.make_request(city)
        if response.status_code != 200:
            await self.handle_error_response(update, context, response)
            return
        await self.handle_success_response(update, context, city, response)


    async def handle_success_response(self, update, context, city, response):
        data = response.json()
        message = self.create_message(city, data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


    def create_message(self, city, data):
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        message = localization_handler.get_localized_text("weather_request_description_message", 
                                                          city=city, weather_description=weather_description, temperature=temperature)
        message += '\n\n' + self.get_open_ai_tips(message)
        return message


    def get_open_ai_tips(self, message):
        request_text = localization_handler.get_localized_text("weather_openai_tips_request", message=message)
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_text_request(request_text)

        tips_and_information: str = localization_handler.get_localized_text("tips_and_information_request_error_message")

        if response is not None:
            # Extract the sentiment analysis result
            tips_and_information = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    tips_and_information += chunk.choices[0].delta.content
                    
        return tips_and_information


    async def handle_error_response(self, update, context, response):
        message = localization_handler.get_localized_text("weather_request_error_message")
        print(f'Weather request returned status code: {response.status_code}. Problem is {response.reason}')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
