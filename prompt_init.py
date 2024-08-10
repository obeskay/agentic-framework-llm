import openai
import speech_recognition as sr
import pyttsx3

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
    while True:
        command = listen()
        if command:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": command}]
            )
            reply = response['choices'][0]['message']['content']
            print(f"Respuesta: {reply}")
            speak(reply)

if __name__ == '__main__':
    main()
