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

def self_improvement():
    improvement_prompt = "¿Cómo puedo mejorar mi código o lógica para ser más eficiente?"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": improvement_prompt}]
    )
    improvement_suggestion = response['choices'][0]['message']['content']
    print(f"Sugerencia de mejora: {improvement_suggestion}")
    speak(improvement_suggestion)

def main():
    while True:
        command = listen()
        if command:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": command}]
            )
            reply = response['choices'][0]['message']['content']
            print(f"Respuesta: {reply}")
            speak(reply)
            self_improvement()  # Llamar a la función de auto-mejora después de cada respuesta

if __name__ == '__main__':
    main()
