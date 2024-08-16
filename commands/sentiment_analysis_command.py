from commands.base_command import Command 
from telegram import Update
from telegram.ext import CallbackContext
from api_requests.open_ai_request import OpenAIRequest


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