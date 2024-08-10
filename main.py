import asyncio
import logging
import subprocess
from flask import Flask, request, jsonify, render_template
from user_interface import UserInterface
from agents.base_agent import BaseAgent
from tools.read_file import read_file
from tools.write_file import write_file
from tools.search_and_replace import search_and_replace

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

agent = BaseAgent()

def update_git_repository():
    try:
        logger.info("Actualizando el repositorio Git...")
        subprocess.run(["git", "fetch", "origin"], check=True)
        subprocess.run(["git", "reset", "--hard", "origin/main"], check=True)
        logger.info("Repositorio Git actualizado exitosamente.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al actualizar el repositorio Git: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
async def send_message():
    try:
        content = request.json.get('message')
        if not content:
            logger.warning("Received empty message")
            return jsonify({'error': 'Message content is required'}), 400

        logger.info(f"Received message: {content}")
        
        if agent.assistant_id is None:
            logger.error("Assistant not initialized")
            return jsonify({'error': 'Assistant not initialized. Please create an assistant first.'}), 500
        
        logger.info(f"Sending message to assistant {agent.assistant_id}")
        response = await agent.send_message(None, content)
        
        if response is None:
            logger.error("Failed to get response from assistant")
            return jsonify({'error': 'Failed to get response from assistant. Please try again later.'}), 500
        
        logger.info(f"Received response from assistant: {response}")
        return jsonify(response)
    except Exception as e:
        logger.exception(f"Unexpected error in send_message: {str(e)}")
        error_details = str(e)
        if hasattr(e, 'response'):
            error_details += f"\nResponse status: {e.response.status_code}"
            error_details += f"\nResponse content: {e.response.text}"
        return jsonify({'error': f'An unexpected error occurred: {error_details}'}), 500

@app.route('/create_assistant', methods=['POST'])
async def create_assistant():
    name = request.json['name']
    instructions = request.json['instructions']
    tools = request.json['tools']
    assistant = await agent.create_assistant(name, instructions, tools)
    return jsonify(assistant)

@app.route('/api/read_file', methods=['POST'])
def handle_read_file():
    data = request.get_json()
    file_path = data.get('file_path')
    if not file_path:
        return jsonify({'error': 'Missing file_path in request'}), 400

    content, success = read_file(file_path)
    if success:
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'Failed to read file'}), 500

@app.route('/api/write_file', methods=['POST'])
def handle_write_file():
    data = request.get_json()
    file_path = data.get('file_path')
    content = data.get('content')
    if not file_path or content is None:
        return jsonify({'error': 'Missing file_path or content in request'}), 400

    success, message = write_file(file_path, content)
    if success:
        return jsonify({'message': 'File written successfully'})
    else:
        return jsonify({'error': f'Failed to write file: {message}'}), 500

@app.route('/api/search_and_replace', methods=['POST'])
def handle_search_and_replace():
    data = request.get_json()
    file_path = data.get('file_path')
    search_text = data.get('search_text')
    replace_text = data.get('replace_text')
    if not file_path or not search_text or not replace_text:
        return jsonify({'error': 'Missing file_path, search_text, or replace_text in request'}), 400

    content, success = search_and_replace(file_path, search_text, replace_text)
    if success:
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'Failed to perform search and replace'}), 500

async def setup_assistant():
    try:
        logger.info("Setting up assistant...")
        assistant = await agent.create_assistant(
            name="Task Assistant",
            instructions="You are a helpful assistant that can break down complex tasks and provide step-by-step guidance.",
            tools=[
                {"type": "code_interpreter"},
                {"type": "function", "function": {"name": "read_file", "description": "Read the contents of a file"}},
                {"type": "function", "function": {"name": "write_file", "description": "Write content to a file"}},
                {"type": "function", "function": {"name": "search_and_replace", "description": "Search and replace text in a file"}}
            ]
        )
        
        if assistant is None:
            logger.error("Failed to create assistant. Exiting.")
            return False
        logger.info(f"Assistant created successfully with ID: {agent.assistant_id}")
        return True
    except Exception as e:
        logger.exception(f"Error creating assistant: {str(e)}")
        return False

async def run_user_interface():
    ui = UserInterface()
    await ui.run()

def run_flask():
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

async def main():
    try:
        update_git_repository()
        
        if not await setup_assistant():
            logger.error("Failed to set up assistant. Exiting.")
            return

        logger.info("Starting user interface...")
        ui_task = asyncio.create_task(run_user_interface())

        logger.info("Starting Flask server...")
        await asyncio.to_thread(run_flask)

        await ui_task
    except Exception as e:
        logger.exception(f"Unexpected error in main function: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
