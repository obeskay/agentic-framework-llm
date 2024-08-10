from services.openai_service import OpenAIService

class BaseAgent:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.openai_service = OpenAIService(api_key, model)

    def send_message(self, message):
        return self.openai_service.send_message(message)
