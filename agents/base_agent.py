import asyncio
from openai import OpenAI

class BaseAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    async def communicate(self, messages):
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=300,
            )
            self._critique_response(response)
            return response.choices[0].message.content
        except Exception as e:
            self._handle_error(e)
            return None

    def _handle_error(self, error):
        print(f"Error in API call: {error}")

    def _critique_response(self, response):
        # Basic critique logic to check for coherence and relevance
        content = response.choices[0].message.content
        if not content or len(content.split()) < 5:  # Simple check for coherence
            print("Response seems too short or incoherent.")
        # Additional checks for relevance can be added here
