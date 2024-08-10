import openai

class OpenAIService:
    def __init__(self, api_key, model="gpt-4o-mini"):
        openai.api_key = api_key
        self.model = model

    def send_message(self, message):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']
