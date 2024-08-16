from commands_module.base_command import Command 
from telegram.ext import CallbackContext
from telegram import Update
from api_requests_module.open_ai_request import OpenAIRequest
from api_requests_module.weather_request import OpenWeatherMapRequest


class WeatherCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):

        city = "Montevideo"  # You can modify this to get the city from user input
        """
        api_key = os.getenv('OPEN_WEATHER_MAP_API_KEY')
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        response = requests.get(url)
        """
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


    async def handle_error_response(self, update, context, response):
        message = "No se pudo obtener la información del clima. Por favor, intenta de nuevo más tarde."
        print(f'Weather request returned status code: {response.status_code}. Problem is {response.reason}')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
