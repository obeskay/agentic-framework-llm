import requests
import logging

logging.basicConfig(level=logging.INFO)

def call_tool(tool_name, params):
    try:
        url = f'http://localhost:5000/api/{tool_name}'
        logging.info(f"Calling tool {tool_name} with params: {params}")
        response = requests.post(url, json=params)
        response.raise_for_status()  # Raise an error for bad status codes
        logging.info(f"Tool {tool_name} call successful. Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling tool {tool_name}: {e}")
        return None

# Example usage
result = call_tool('write_file', {'file_path': '/tmp/example.txt', 'content': 'Hello, World!'})
if result:
    logging.info(f"Success: {result}")
else:
    logging.error("Failed to call tool.")
