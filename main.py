
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, filters, MessageHandler
from commands_module import commands, bot_invoker
import os
from dotenv import load_dotenv



# Initialize the invoker
invoker = bot_invoker.BotInvoker()

# Register commands
invoker.register('¡Quiero saber el clima!☀️', commands.WeatherCommand())
invoker.register('¡Quiero contar!🔢', commands.CounterCommand())
invoker.register('¡Analizar sentimiento!🤔', commands.SentimentAnalysisCommand())


# Define a function to handle the main menu
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in context.bot_data:
        context.bot_data[chat_id] = []
   
    # Load environment variables from .env file
    load_dotenv()

    await init_keyboard(update)
    

async def init_keyboard(update):
    keyboard = [
        [KeyboardButton("¡Quiero saber el clima!☀️")],
        [KeyboardButton("¡Quiero contar!🔢")],
        [KeyboardButton("¡Analizar sentimiento!🤔")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text('¡Hola! ¿Qué necesitas? 😊', reply_markup=reply_markup)

# Define a function to handle button presses
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in context.bot_data:
        context.bot_data[chat_id] = []
    context.bot_data[chat_id].append(update.message.text)
    command_name = update.message.text
    await invoker.execute(command_name, update, context)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Set up the updater and dispatcher
app = Application.builder().token(os.getenv('TELEGRAM_API_KEY')).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
# Errors
#app.add_error_handler(error)

# Start the bot
if __name__ == '__main__':
    print('Starting bot...')
    app.run_polling(poll_interval=2.5)
