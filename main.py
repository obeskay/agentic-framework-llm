import requests
import logging
import os

logging.basicConfig(level=logging.INFO)

def call_tool(tool_name, params):
    try:
        url = f'http://localhost:5000/api/{tool_name}'
        logging.info(f"Calling tool {tool_name} with params: {params}")
        response = requests.post(url, json=params)
        response.raise_for_status()  # Raise an error for bad status codes
        logging.info(f"Tool {tool_name} call successful. Response: {response.json()}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logging.error(f"Error 403 Forbidden: No tienes permiso para acceder a {url}")
            logging.error(f"Asegúrate de que tienes los permisos necesarios y que la ruta del archivo es correcta.")
        else:
            logging.error(f"Error HTTP llamando a la herramienta {tool_name}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error llamando a la herramienta {tool_name}: {e}")
        return None

# Ejemplo de uso
home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, 'example.txt')
result = call_tool('write_file', {'file_path': file_path, 'content': 'Hello, World!'})
if result:
    logging.info(f"Éxito: {result}")
else:
    logging.error("No se pudo llamar a la herramienta.")
