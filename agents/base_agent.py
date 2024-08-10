import os
import logging
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional

class BaseAgent:
    def __init__(self, model: str = "gpt-4-1106-preview"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.assistant_id = None
        self.thread_id = None

    async def create_assistant(self, name: str, instructions: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            assistant = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            self.assistant_id = assistant.id
            return assistant.dict()
        except Exception as e:
            self._handle_error(e)
            return None

    async def create_thread(self) -> Dict[str, Any]:
        try:
            thread = await self.client.beta.threads.create()
            self.thread_id = thread.id
            return thread.dict()
        except Exception as e:
            self._handle_error(e)
            return None

    async def send_message(self, thread_id: Optional[str], content: str) -> Dict[str, Any]:
        try:
            if thread_id is None:
                if self.thread_id is None:
                    thread = await self.create_thread()
                    thread_id = thread['id']
                else:
                    thread_id = self.thread_id

            message = await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                instructions="Please respond to the user's message."
            )
            return await self._wait_for_response(thread_id, run.id)
        except Exception as e:
            self._handle_error(e)
            return None

    async def _wait_for_response(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        while True:
            try:
                run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.status == "completed":
                    messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                    return messages.data[0].dict()
                elif run.status == "failed":
                    raise Exception(f"Run failed: {run.last_error}")
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self._handle_error(e)
                return None

    def _handle_error(self, error: Exception) -> None:
        logging.error(f"Error occurred: {error}", exc_info=True)
        # Implement additional error handling logic if necessary

    def _critique_response(self, response: Dict[str, Any]) -> None:
        if not response or 'content' not in response or not response['content']:
            logging.warning("Response is empty or invalid.")
            return
        content = response['content'][0].text if isinstance(response['content'][0], dict) else response['content'][0]
        if len(content.split()) < 5:
            logging.warning("Response seems too short or incoherent.")
        # Implement more sophisticated criteria for evaluating the response
