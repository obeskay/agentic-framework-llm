from flask import Flask, request, jsonify
from tools.read_file import read_file
from tools.write_file import write_file
from tools.search_and_replace import search_and_replace

app = Flask(__name__)

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

    success = write_file(file_path, content)
    if success:
        return jsonify({'message': 'File written successfully'})
    else:
        return jsonify({'error': 'Failed to write file'}), 500

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
    app.run(host='localhost', port=5000, debug=True)
