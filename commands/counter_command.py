from commands.base_command import Command 
from telegram import Update
from telegram.ext import CallbackContext
from counter import counter

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