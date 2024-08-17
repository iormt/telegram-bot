import os
import config.constants as constants
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, filters, MessageHandler
from commands import bot_invoker, counter_command, free_message_command, sentiment_analysis_command, weather_command
from dotenv import load_dotenv
from history.history import MessageHistory 
from api_requests.open_ai_request import OpenAIRequest


# Define a function to handle the main menu
async def start(update: Update, context: CallbackContext):
    MessageHistory.initialize_message_history(update, context) 

    await init_keyboard(update)


async def init_keyboard(update):
    keyboard = [
        [KeyboardButton("¡Quiero saber el clima!☀️")],
        [KeyboardButton("¡Quiero contar!🔢")],
        [KeyboardButton("¡Analizar sentimiento!🤔")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    message = '¡Hola! ¿Qué necesitas? 😊'
    message += '\nSelecciona una opción del menú o bien escribe tu consulta en un mensaje e intentaré ayudarte.' 
    await update.message.reply_text(message, reply_markup=reply_markup)


# Define a function to handle button presses
async def handle_message(update: Update, context: CallbackContext):
    command_name = update.message.text
    MessageHistory.add_message_to_history(update, context, command_name)
    await invoker.execute(command_name, update, context)


async def handle_voice(update: Update, context: CallbackContext):
    file = await update.message.voice.get_file()
    file_path = await file.download_to_drive()

    # Convert the audio file to text using OpenAI Whisper
    with open(file_path, 'rb') as audio_file:
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_whisper_request(audio_file)
    
    transcription = response.text
    MessageHistory.add_message_to_history(update, context, transcription)
    await invoker.execute(transcription, update, context)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



# Start the bot
if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the invoker
    invoker = bot_invoker.BotInvoker()

    # Register commands to invoker
    invoker.register('¡Quiero saber el clima!☀️', weather_command.WeatherCommand())
    invoker.register('¡Quiero contar!🔢', counter_command.CounterCommand())
    invoker.register('¡Analizar sentimiento!🤔', sentiment_analysis_command.SentimentAnalysisCommand())
    invoker.register('default', free_message_command.FreeMessageCommand())

    # Set up the updater and dispatcher
    app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # Errors
    #app.add_error_handler(error)

    print('Starting bot...')
    app.run_polling(poll_interval=constants.TELEGRAM_BOT_POLL_INTERVALL)
