import asyncio
from openai import OpenAI

class BaseAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    async def communicate(self, messages):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content
