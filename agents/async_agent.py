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
from typing import List, Dict, Any, Callable
from agents.base_agent import BaseAgent

class AsyncAgent(BaseAgent):
    def __init__(self, model: str = "gpt-4o-mini"):
        super().__init__(model)
        self.tasks_queue = asyncio.Queue()

    async def execute_tasks(self, tasks: List[Callable]) -> List[Any]:
        async def worker():
            while True:
                task = await self.tasks_queue.get()
                try:
                    result = await task()
                except Exception as e:
                    result = f"Error: {str(e)}"
                finally:
                    self.tasks_queue.task_done()
                    results.append(result)

        results = []
        workers = [asyncio.create_task(worker()) for _ in range(min(len(tasks), 5))]  # Limit to 5 concurrent tasks

        for task in tasks:
            await self.tasks_queue.put(task)

        await self.tasks_queue.join()

        for w in workers:
            w.cancel()

        return results

    async def handle_conversation(self, thread_id: str) -> Dict[str, Any]:
        try:
            messages = []
            async for message in self._stream_response(thread_id, None):
                messages.append(message)
            return {"thread_id": thread_id, "messages": messages}
        except Exception as e:
            self._handle_error(e)
            return {"thread_id": thread_id, "error": str(e)}

    def run_async_tasks(self, tasks: List[Callable]) -> List[Any]:
        return asyncio.run(self.execute_tasks(tasks))

    async def process_multiple_threads(self, thread_ids: List[str]) -> List[Dict[str, Any]]:
        tasks = [self.handle_conversation(thread_id) for thread_id in thread_ids]
        return await asyncio.gather(*tasks)
