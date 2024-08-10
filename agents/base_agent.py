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
        # Placeholder for response critique logic
        # This could involve checking the response for coherence, relevance, etc.
        pass
