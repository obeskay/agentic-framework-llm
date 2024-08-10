from agents.base_agent import BaseAgent

class SelfImprovementAgent:
    def __init__(self, agent):
        self.agent = agent

    def self_improvement(self):
        improvement_prompt = "¿Cómo puedo mejorar mi código o lógica para ser más eficiente?"
        suggestion = self.agent.send_message(improvement_prompt)
        print(f"Sugerencia de mejora: {suggestion}")
        speak(suggestion)
