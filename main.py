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
import asyncio
from agents.base_agent import BaseAgent
from agents.self_improvement_agent import SelfImprovementAgent
from agents.async_agent import AsyncAgent
from tools.memory_manager import MemoryManager
try:
    from tools.image_processing import encode_image, analyze_package_image, pdf_to_images, extract_text_from_image
except ImportError:
    logging.warning("PIL no está instalado. Las funciones de procesamiento de imágenes no estarán disponibles.")
    encode_image = analyze_package_image = pdf_to_images = extract_text_from_image = None
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        base_agent = BaseAgent()
        self_improvement_agent = SelfImprovementAgent()
        async_agent = AsyncAgent()
        memory_manager = MemoryManager()

        logging.info("Iniciando análisis del código base...")
        await self_improvement_agent.analyze_codebase()
        logging.info("Análisis del código base completado.")

        logging.info("Iniciando mejora del código base...")
        await self_improvement_agent.improve_codebase()
        logging.info("Mejora del código base completada.")

        if encode_image and analyze_package_image and pdf_to_images and extract_text_from_image:
            image_path = "path/to/image.jpg"
            logging.info(f"Procesando imagen: {image_path}")
            encoded_image = encode_image(image_path)
            analysis_result = analyze_package_image(image_path)
            logging.info(f"Resultado del análisis de la imagen: {analysis_result}")

            pdf_path = "path/to/document.pdf"
            logging.info(f"Convirtiendo PDF a imágenes: {pdf_path}")
            pdf_images = pdf_to_images(pdf_path)
            for i, image in enumerate(pdf_images):
                text = extract_text_from_image(image)
                logging.info(f"Texto extraído de la página {i+1}: {text[:100]}...")  # Mostrar los primeros 100 caracteres
        else:
            logging.warning("Las funciones de procesamiento de imágenes no están disponibles debido a la falta de dependencias.")

        # Ejemplo de uso del AsyncAgent
        tasks = [
            lambda: base_agent.send_message("thread_id_1", "Hello, how are you?"),
            lambda: base_agent.send_message("thread_id_2", "What's the weather like today?"),
            lambda: self_improvement_agent.generate_new_tool("A tool for sentiment analysis")
        ]
        results = async_agent.run_async_tasks(tasks)
        for i, result in enumerate(results):
            logging.info(f"Resultado de la tarea {i+1}: {result}")

        # Ejemplo de uso del MemoryManager
        memory_manager.add_to_stm("Información importante a corto plazo")
        memory_manager.add_to_ltm("Información importante a largo plazo")
        memory_manager.save_session("session.json")

        logging.info("Búsqueda en la memoria...")
        search_results = memory_manager.search_memory("importante")
        logging.info(f"Resultados de la búsqueda: {search_results}")

    except Exception as e:
        logging.error(f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
