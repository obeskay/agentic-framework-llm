import asyncio
from user_interface import UserInterface
from agents.base_agent import BaseAgent

async def main():
    agent = BaseAgent()
    
    # Create an assistant first
    assistant = await agent.create_assistant(
        name="Task Assistant",
        instructions="You are a helpful assistant that can break down complex tasks and provide step-by-step guidance.",
        tools=[{"type": "code_interpreter"}]  # Using a valid tool type
    )
    
    if assistant is None:
        print("Failed to create assistant. Exiting.")
        return

    ui = UserInterface()
    await ui.run()

if __name__ == "__main__":
    asyncio.run(main())
