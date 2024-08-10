import os
import logging
import asyncio
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional

class BaseAgent:
    def __init__(self, model: str = "gpt-4-1106-preview"):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.assistant_id = None
        self.thread_id = None
        self.max_retries = 3
        self.retry_delay = 2

    async def create_assistant(self, name: str, instructions: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                valid_tools = [
                    tool for tool in tools
                    if tool.get('type') in ['code_interpreter', 'function', 'retrieval']
                ]
                assistant = await self.client.beta.assistants.create(
                    name=name,
                    instructions=instructions,
                    tools=valid_tools,
                    model=self.model
                )
                self.assistant_id = assistant.id
                return assistant.model_dump()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    self._handle_error(e, "Failed to create assistant")
                    return None
                await asyncio.sleep(self.retry_delay)

    async def create_thread(self) -> Dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                thread = await self.client.beta.threads.create()
                self.thread_id = thread.id
                return thread.model_dump()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    self._handle_error(e, "Failed to create thread")
                    return None
                await asyncio.sleep(self.retry_delay)

    async def send_message(self, thread_id: Optional[str], content: str) -> Dict[str, Any]:
        try:
            if thread_id is None:
                if self.thread_id is None:
                    logging.info("Creating new thread")
                    thread = await self.create_thread()
                    if thread is None:
                        raise ValueError("Failed to create a new thread")
                    thread_id = thread['id']
                else:
                    thread_id = self.thread_id

            logging.info(f"Creating message in thread {thread_id}")
            message = await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
            logging.info(f"Message created: {message}")
            
            if self.assistant_id is None:
                raise ValueError("Assistant ID is not set. Please create an assistant first.")

            logging.info(f"Creating run with assistant {self.assistant_id}")
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                instructions="Please respond to the user's message."
            )
            logging.info(f"Run created: {run}")
            logging.info(f"Waiting for response from run {run.id}")
            return await self._wait_for_response(thread_id, run.id)
        except Exception as e:
            self._handle_error(e, "Error sending message")
            raise  # Re-raise the exception to be caught in the main.py

    async def _wait_for_response(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        max_wait_time = 300  # 5 minutes
        start_time = asyncio.get_event_loop().time()
        while True:
            try:
                run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.status == "completed":
                    messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                    response = messages.data[0].model_dump()
                    self._critique_response(response)
                    return response
                elif run.status == "failed":
                    raise Exception(f"Run failed: {run.last_error}")
                elif asyncio.get_event_loop().time() - start_time > max_wait_time:
                    raise TimeoutError("Response wait time exceeded")
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self._handle_error(e, "Error waiting for response")
                return None

    def _handle_error(self, error: Exception, context: str) -> None:
        logging.error(f"{context}: {error}", exc_info=True)
        # Implement additional error handling logic if necessary

    def _critique_response(self, response: Dict[str, Any]) -> None:
        if not response or 'content' not in response or not response['content']:
            logging.warning("Response is empty or invalid.")
            return
        content = response['content'][0].text if isinstance(response['content'][0], dict) else response['content'][0]
        if len(content.split()) < 5:
            logging.warning("Response seems too short or incoherent.")
        # Implement more sophisticated criteria for evaluating the response

    async def list_assistants(self) -> List[Dict[str, Any]]:
        try:
            assistants = await self.client.beta.assistants.list()
            return [assistant.model_dump() for assistant in assistants.data]
        except Exception as e:
            self._handle_error(e, "Error listing assistants")
            return []

    async def delete_assistant(self, assistant_id: str) -> bool:
        try:
            await self.client.beta.assistants.delete(assistant_id)
            if self.assistant_id == assistant_id:
                self.assistant_id = None
            return True
        except Exception as e:
            self._handle_error(e, f"Error deleting assistant {assistant_id}")
            return False
