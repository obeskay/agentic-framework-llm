from agents.base_agent import BaseAgent
from agents.self_improvement_agent import SelfImprovementAgent
from agents.async_agent import AsyncAgent
from tools.memory_manager import MemoryManager
from services.speech_service import listen, speak

def main():
    base_agent = BaseAgent()
    memory_manager = MemoryManager()
    self_improvement_agent = SelfImprovementAgent(base_agent)
    async_agent = AsyncAgent()

    while True:
        command = listen()
        if command:
            reply = base_agent.send_message(command)
            print(f"Respuesta: {reply}")
            speak(reply)
            self_improvement_agent.self_improvement()

if __name__ == '__main__':
    main()
