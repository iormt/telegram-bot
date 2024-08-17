from openai import OpenAI
import os
from ratelimit import limits, sleep_and_retry
from config import constants


class OpenAIRequest:
    def __init__(self):
        self.api_key = os.getenv('OPEN_AI_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set the OPEN_AI_API_KEY environment variable.")

        self.client = OpenAI(
            api_key=self.api_key
        )
    @sleep_and_retry
    @limits(calls=5, period=60)


    def make_text_request(self, request_text):
        try:
            response = self.client.chat.completions.create(
                model=constants.OPEN_AI_GPT_MODEL,
                messages=[
                    {"role": "user", "content": f"{request_text}"}
                ],
                stream=True
            )
            return response
        except Exception as e:
            print(f'Error making API request: {e}')
            return None


    def make_whisper_request(self, audio_file):
        try:
            response = self.client.audio.transcriptions.create(
                model=constants.OPEN_AI_WHISPER_MODEL,
                file=audio_file
            )
            return response
        except Exception as e:
            print(f'Error making API request: {e}')
            return None