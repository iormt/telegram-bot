
from constants_module import constants 
from openai import OpenAI
import os

class OpenAIRequest:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('OPEN_AI_API_KEY')
        )

    def make_request(self, request_text):
        return self.client.chat.completions.create(
            model=constants.OPEN_AI_MODEL,
            messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{request_text}"}
            ],
            stream=True
        )