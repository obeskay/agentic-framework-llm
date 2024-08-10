import requests

def call_tool(tool_name, params):
    try:
        response = requests.post(f'http://localhost:5000/tools/{tool_name}', json=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling tool {tool_name}: {e}")
        return None

# Example usage
result = call_tool('write_file', {'file_path': 'example.txt', 'content': 'Hello, World!'})
if result:
    print(f"Success: {result}")
else:
    print("Failed to call tool.")
