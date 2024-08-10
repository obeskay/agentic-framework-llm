import asyncio
from .base_agent import BaseAgent

class AsyncAgent(BaseAgent):
    async def run_tasks(self, tasks):
        return await asyncio.gather(*tasks)
