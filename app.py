from flask import Flask, request, jsonify
import logging
import os
from tools.read_file import read_file
from tools.write_file import write_file
from tools.search_and_replace import search_and_replace

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

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

    logging.debug(f"Attempting to write to file: {file_path}")
    logging.debug(f"File exists: {os.path.exists(file_path)}")
    logging.debug(f"File is writable: {os.access(file_path, os.W_OK) if os.path.exists(file_path) else 'N/A'}")
    logging.debug(f"Directory is writable: {os.access(os.path.dirname(file_path), os.W_OK)}")

    success, message = write_file(file_path, content)
    if success:
        logging.info(f"Successfully wrote to file: {file_path}")
        return jsonify({'message': 'File written successfully'})
    else:
        logging.error(f"Failed to write to file: {file_path}. Error: {message}")
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

@app.route('/', methods=['GET'])
def home():
    return "Flask server is running", 200

if __name__ == '__main__':
    logging.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
