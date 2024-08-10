import requests
import logging
import os

logging.basicConfig(level=logging.DEBUG)

def call_tool(tool_name, params):
    try:
        url = f'http://localhost:5001/api/{tool_name}'
        logging.info(f"Llamando a la herramienta {tool_name} con parámetros: {params}")
        logging.debug(f"URL completa: {url}")
        response = requests.post(url, json=params)
        logging.debug(f"Código de estado de la respuesta: {response.status_code}")
        logging.debug(f"Headers de la respuesta: {response.headers}")
        logging.debug(f"Contenido de la respuesta: {response.text}")
        response.raise_for_status()  # Lanza un error para códigos de estado incorrectos
        if response.text:
            logging.info(f"Llamada a la herramienta {tool_name} exitosa. Respuesta: {response.json()}")
        else:
            logging.warning(f"La respuesta del servidor está vacía para la herramienta {tool_name}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logging.error(f"Error 403 Forbidden: No tienes permiso para acceder a {url}")
            logging.error(f"Headers de la respuesta: {e.response.headers}")
            logging.error(f"Contenido de la respuesta: {e.response.text}")
            logging.error(f"Asegúrate de que tienes los permisos necesarios y que la ruta del archivo es correcta.")
        else:
            logging.error(f"Error HTTP llamando a la herramienta {tool_name}: {e}")
            logging.error(f"Headers de la respuesta: {e.response.headers}")
            logging.error(f"Contenido de la respuesta: {e.response.text}")
        return None
    except requests.exceptions.ConnectionError:
        logging.error(f"Error de conexión. Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:5000")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error llamando a la herramienta {tool_name}: {e}")
        return None

# Ejemplo de uso
home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, 'example.txt')

# Verificar si el directorio es escribible
if not os.access(os.path.dirname(file_path), os.W_OK):
    logging.error(f"No tienes permisos de escritura en el directorio: {os.path.dirname(file_path)}")
else:
    result = call_tool('write_file', {'file_path': file_path, 'content': 'Hello, World!'})
    if result:
        logging.info(f"Éxito: {result}")
    else:
        logging.error("No se pudo llamar a la herramienta.")

# Verificar si el servidor Flask está ejecutándose
try:
    response = requests.get('http://localhost:5001')
    logging.info(f"El servidor Flask está ejecutándose. Código de estado: {response.status_code}")
    logging.info(f"Headers de la respuesta: {response.headers}")
    logging.info(f"Contenido de la respuesta: {response.text}")
except requests.exceptions.ConnectionError:
    logging.error("No se pudo conectar al servidor Flask. Asegúrate de que esté ejecutándose en http://localhost:5001")
from agents.base_agent import BaseAgent
from agents.self_improvement_agent import SelfImprovementAgent
from agents.async_agent import AsyncAgent
from tools.memory_manager import MemoryManager
from tools.image_processing import encode_image, analyze_package_image

def main():
    base_agent = BaseAgent()
    self_improvement_agent = SelfImprovementAgent()
    async_agent = AsyncAgent()
    memory_manager = MemoryManager()

    # Example usage
    self_improvement_agent.analyze_codebase()
    
    image_path = "path/to/image.jpg"
    encoded_image = encode_image(image_path)
    analysis_result = analyze_package_image(image_path)

    # Add more functionality as needed

if __name__ == "__main__":
    main()
