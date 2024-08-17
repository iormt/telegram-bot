from telegram import Update
from telegram.ext import CallbackContext


class MessageHistory():
    def add_message_to_history(update: Update, context: CallbackContext, message: str):
        chat_id = update.effective_chat.id
        if chat_id not in context.bot_data:
            context.bot_data[chat_id] = []
        context.bot_data[chat_id].append(message)

        
    def initialize_message_history(update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        if chat_id not in context.bot_data:
            context.bot_data[chat_id] = []