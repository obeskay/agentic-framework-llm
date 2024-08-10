import openai
import speech_recognition as sr
import pyttsx3
import threading

# Configuración de OpenAI
openai.api_key = 'tu_api_key_aqui'

# Inicialización de TTS
engine = pyttsx3.init()

class BaseAgent:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def send_message(self, message):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']

class MemoryManager:
    def __init__(self):
        self.short_term_memory = []
        self.long_term_memory = {}

    def add_to_memory(self, key, value):
        self.long_term_memory[key] = value

    def get_from_memory(self, key):
        return self.long_term_memory.get(key, None)

class SelfImprovementAgent:
    def __init__(self, agent):
        self.agent = agent

    def self_improvement(self):
        improvement_prompt = "¿Cómo puedo mejorar mi código o lógica para ser más eficiente?"
        suggestion = self.agent.send_message(improvement_prompt)
        print(f"Sugerencia de mejora: {suggestion}")
        speak(suggestion)

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

    while True:
        command = listen()
        if command:
            reply = base_agent.send_message(command)
            print(f"Respuesta: {reply}")
            speak(reply)
            self_improvement_agent.self_improvement()  # Llamar a la función de auto-mejora después de cada respuesta

if __name__ == '__main__':
    main()
