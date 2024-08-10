import logging
from agents.async_agent import AsyncAgent

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

agent = AsyncAgent()

def setup_assistant():
    try:
        logger.info("Setting up assistant...")
        assistant = agent.create_assistant(
            name="Task Assistant",
            instructions="You are a helpful assistant that can break down complex tasks and provide step-by-step guidance.",
            tools=[
                {"type": "code_interpreter"},
                {"type": "function", "function": {"name": "read_file", "description": "Read the contents of a file"}},
                {"type": "function", "function": {"name": "write_file", "description": "Write content to a file"}},
                {"type": "function", "function": {"name": "search_and_replace", "description": "Search and replace text in a file"}}
            ]
        )
        
        if assistant is None or 'id' not in assistant:
            logger.error("Failed to create assistant.")
            return False
        
        agent.assistant_id = assistant['id']
        logger.info(f"Assistant created successfully with ID: {assistant['id']}")
        return True
    except Exception as e:
        logger.exception(f"Error creating assistant: {str(e)}")
        return False

        response = agent.send_message(None, message)
    try:
        response = agent.send_message(None, message)
        if response and 'content' in response:
            return response['content'][0].text
        else:
            logger.error("Failed to get response from assistant")
            return None
    except Exception as e:
        logger.exception(f"Error sending message: {str(e)}")
        return None

if __name__ == "__main__":
    if setup_assistant():
        logger.info("Assistant setup completed successfully.")
    else:
        logger.error("Failed to set up assistant.")