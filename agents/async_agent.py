import asyncio
from .base_agent import BaseAgent

class AsyncAgent(BaseAgent):
    async def run_tasks(self, tasks):
        try:
            return await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(f"Error in running tasks: {e}")
            return []
