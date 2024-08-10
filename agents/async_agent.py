import asyncio
from .base_agent import BaseAgent

class AsyncAgent(BaseAgent):
    async def run_tasks(self, tasks):
        try:
            return await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(f"Error in running tasks: {e}")
            return []
import asyncio
from agents.base_agent import BaseAgent

class AsyncAgent(BaseAgent):
    def __init__(self, model="gpt-4o-mini"):
        super().__init__(model)

    async def execute_tasks(self, tasks):
        # Implementation for executing tasks in parallel
        pass

    async def handle_conversation(self, thread_id):
        # Implementation for handling asynchronous conversations
        pass

    def run_async_tasks(self, tasks):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.execute_tasks(tasks))
