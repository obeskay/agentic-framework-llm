import asyncio
from flask import Flask, request, jsonify, render_template
from user_interface import UserInterface
from agents.base_agent import BaseAgent
from tools.read_file import read_file
from tools.write_file import write_file
from tools.search_and_replace import search_and_replace
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

agent = BaseAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
async def send_message():
    try:
        content = request.json['message']
        logging.info(f"Received message: {content}")
        
        if agent.assistant_id is None:
            logging.error("Assistant not initialized")
            return jsonify({'error': 'Assistant not initialized'}), 500
        
        logging.info(f"Sending message to assistant {agent.assistant_id}")
        response = await agent.send_message(None, content)
        
        if response is None:
            logging.error("Failed to get response from assistant")
            return jsonify({'error': 'Failed to get response from assistant'}), 500
        
        logging.info(f"Received response from assistant: {response}")
        return jsonify(response)
    except Exception as e:
        logging.exception(f"Error in send_message: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

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
            print("Failed to create assistant. Exiting.")
            return False
        print(f"Assistant created successfully with ID: {agent.assistant_id}")
        return True
    except Exception as e:
        print(f"Error creating assistant: {str(e)}")
        return False

async def run_user_interface():
    ui = UserInterface()
    await ui.run()

def run_flask():
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

async def main():
    if not await setup_assistant():
        return

    # Ejecutar la interfaz de usuario en un hilo separado
    ui_task = asyncio.create_task(run_user_interface())

    # Ejecutar Flask en el hilo principal
    await asyncio.to_thread(run_flask)

    # Esperar a que la interfaz de usuario termine (si es necesario)
    await ui_task

if __name__ == "__main__":
    asyncio.run(main())
