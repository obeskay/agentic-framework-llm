import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.async_agent import AsyncAgent
from tools.read_file import read_file
from tools.write_file import write_file
from tools.search_and_replace import search_and_replace
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api/ routes
logging.basicConfig(level=logging.DEBUG)

agent = AsyncAgent()

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Server is running"}), 200

@app.route('/api/send_message', methods=['POST'])
def send_message():
    try:
        app.logger.debug(f"Received request: {request.json}")
        content = request.json.get('message')
        if not content:
            return jsonify({'error': 'Message content is required'}), 400

        if agent.assistant_id is None:
            return jsonify({'error': 'Assistant not initialized. Please create an assistant first.'}), 500
        
        app.logger.debug(f"Sending message to agent: {content}")
        response = agent.send_message(None, content)
        app.logger.debug(f"Received response from agent: {response}")
        
        if response is None:
            return jsonify({'error': 'Failed to get response from assistant. Please try again later.'}), 500
        
        return jsonify(response)
    except Exception as e:
        error_details = str(e)
        if hasattr(e, 'response'):
            error_details += f"\nResponse status: {e.response.status_code}"
            error_details += f"\nResponse content: {e.response.text}"
        app.logger.error(f"An error occurred: {error_details}")
        return jsonify({'error': f'An unexpected error occurred: {error_details}'}), 500
    except Exception as e:
        error_details = str(e)
        if hasattr(e, 'response'):
            error_details += f"\nResponse status: {e.response.status_code}"
            error_details += f"\nResponse content: {e.response.text}"
        app.logger.error(f"An error occurred: {error_details}")
        return jsonify({'error': f'An unexpected error occurred: {error_details}'}), 500

@app.route('/api/create_assistant', methods=['POST'])
def create_assistant():
    try:
        app.logger.debug(f"Received request to create assistant: {request.json}")
        name = request.json['name']
        instructions = request.json['instructions']
        tools = request.json['tools']
        assistant = agent.create_assistant(name, instructions, tools)
        app.logger.debug(f"Created assistant: {assistant}")
        return jsonify(assistant)
    except Exception as e:
        app.logger.error(f"Error creating assistant: {str(e)}")
        return jsonify({'error': f'Failed to create assistant: {str(e)}'}), 500

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)