import logging
from agents.base_agent import BaseAgent

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

agent = BaseAgent()

def setup_assistant():
    try:
        logger.info("Setting up assistant...")
        retries = 0
        for _ in range(agent.max_retries):
            try:
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
                    logger.error("Failed to create assistant. Retrying...")
                    continue
                agent.assistant_id = assistant['id']
                logger.info(f"Assistant created successfully with ID: {assistant['id']}")
                break
            except Exception as e:
                logger.exception(f"Error creating assistant: {str(e)}")
                if hasattr(e, 'response'):
                    logger.error(f"Response status: {e.response.status_code}")
                    logger.error(f"Response content: {e.response.text}")
        else:
            logger.error("Failed to create assistant after multiple retries. Exiting.")
            return False
        logger.info(f"Assistant created successfully with ID: {assistant['id']}")
        break
    except Exception as e:
        logger.exception(f"Error creating assistant: {str(e)}")
        if hasattr(e, 'response'):
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        return False

if __name__ == "__main__":
    setup_assistant()
