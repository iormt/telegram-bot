from commands.base_command import Command 
from telegram import Update
from telegram.ext import CallbackContext
from api_requests.open_ai_request import OpenAIRequest
from localizations import localization_handler


class SentimentAnalysisCommand(Command):
    async def execute(self, update: Update, context: CallbackContext):
        
        # Collect the conversation history
        chat_id = update.effective_chat.id
        messages = context.bot_data.get(chat_id, [])
        
        # Prepare the conversation text
        conversation_text = "\n".join(messages)

        # Prepare request text 
        request_text = localization_handler.get_localized_text("sentiment_analysis_request")
        request_text += f'\n\n{conversation_text}'
        # Send the conversation to OpenAI for sentiment analysis
        open_ai_requests = OpenAIRequest()
        response = open_ai_requests.make_text_request(request_text)

        # Set sentiment analysis default message
        sentiment_analysis: str = localization_handler.get_localized_text("sentiment_analysis_request_error")
        
        # Extract the response text
        if response is not None:
            sentiment_analysis = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    sentiment_analysis += chunk.choices[0].delta.content
        

        # Send the result back to the user
        await context.bot.send_message(chat_id=chat_id, text=sentiment_analysis)