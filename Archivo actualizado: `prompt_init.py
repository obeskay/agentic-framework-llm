import openai
import speech_recognition as sr
import pyttsx3
import threading
from agents.base_agent import BaseAgent
from agents.self_improvement_agent import SelfImprovementAgent
from tools.memory_manager import MemoryManager
from tools.image_processing import ImageProcessing  # Importar el módulo de procesamiento de imágenes
from agents.async_agent import AsyncAgent  # Importar el agente asíncrono

# Configuración de OpenAI
openai.api_key = 'tu_api_key_aqui'

# Inicialización de TTS
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Has dicho: {text}")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError as e:
            print(f"Error al solicitar resultados de Google Speech Recognition; {e}")
            return None

def main():
    base_agent = BaseAgent()
    memory_manager = MemoryManager()
    self_improvement_agent = SelfImprovementAgent(base_agent)
    async_agent = AsyncAgent()  # Crear instancia del agente asíncrono

    while True:
        command = listen()
        if command:
            reply = base_agent.send_message(command)
            print(f"Respuesta: {reply}")
            speak(reply)
            self_improvement_agent.self_improvement()  # Llamar a la función de auto-mejora después de cada respuesta

if __name__ == '__main__':
    main()
