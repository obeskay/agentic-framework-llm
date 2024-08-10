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
import asyncio
from openai import OpenAI
from typing import List, Dict, Any, AsyncGenerator

class BaseAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.assistant_id = None  # Add this line

    async def create_assistant(self, name: str, instructions: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            assistant = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            return assistant
        except Exception as e:
            self._handle_error(e)
            return None

    async def create_thread(self) -> Dict[str, Any]:
        try:
            thread = await self.client.beta.threads.create()
            return thread
        except Exception as e:
            self._handle_error(e)
            return None

    async def send_message(self, thread_id: str | None, content: str, stream: bool = False) -> Dict[str, Any]:
        try:
            if thread_id is None:
                thread = await self.create_thread()
                thread_id = thread.id

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
            if stream:
                return await self._stream_response(thread_id, run.id)
            else:
                return await self._wait_for_response(thread_id, run.id)
        except Exception as e:
            self._handle_error(e)
            return None

    async def _stream_response(self, thread_id: str, run_id: str) -> AsyncGenerator[str, None]:
        while True:
            try:
                run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.status == "completed":
                    messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                    for message in messages.data:
                        if message.role == "assistant":
                            yield message.content
                    break
                elif run.status == "failed":
                    raise Exception(f"Run failed: {run.last_error}")
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self._handle_error(e)
                break

    async def _wait_for_response(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        while True:
            try:
                run = await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.status == "completed":
                    messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
                    return messages.data[0]
                elif run.status == "failed":
                    raise Exception(f"Run failed: {run.last_error}")
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                self._handle_error(e)
                return None

    def _handle_error(self, error: Exception) -> None:
        print(f"Error: {error}")
        # Aquí podrías implementar un sistema de logging más robusto

    def _critique_response(self, response: Dict[str, Any]) -> None:
        if not response or 'content' not in response:
            print("Response is empty or invalid.")
            return
        content = response['content'][0].text
        if len(content.split()) < 5:
            print("Response seems too short or incoherent.")
        # Aquí podrías implementar criterios más sofisticados para evaluar la respuesta
