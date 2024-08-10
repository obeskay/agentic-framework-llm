import requests

def call_tool(tool_name, params):
    response = requests.post(f'http://localhost:5000/tools/{tool_name}', json=params)
    return response.json()

# Example usage
result = call_tool('write_file', {'file_path': 'example.txt', 'content': 'Hello, World!'})
print(result)
