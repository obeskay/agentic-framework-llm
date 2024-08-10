import openai

class BaseAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def send_message(self, message):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']
