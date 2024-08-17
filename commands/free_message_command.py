from commands.base_command import Command 
from telegram import Update
from telegram.ext import CallbackContext
from api_requests.open_ai_request import OpenAIRequest
from localizations import localization_handler

class FreeMessageCommand(Command):
    async def execute(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        request_text = context.bot_data['free_message']
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_text_request(request_text)
        
        response_text: str = localization_handler.get_localized_text("free_openai_message_request_error")
        if response is not None:
            response_text = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content

        await context.bot.send_message(chat_id=chat_id, text=response_text)