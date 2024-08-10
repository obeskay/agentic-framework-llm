import asyncio
from typing import List
from agents.async_agent import AsyncAgent

class UserInterface:
    def __init__(self):
        self.agent = AsyncAgent()

    def welcome(self):
        print("¡Bienvenido al Asistente de Tareas Complejas!")

    def show_menu(self):
        print("\nMenú de funcionalidades:")
        print("1. Descomponer y ejecutar tarea compleja")
        print("2. Salir")

    async def get_user_input(self):
        return input("Por favor, ingrese el número de la opción deseada: ")

    async def get_complex_task(self):
        return input("Por favor, ingrese su tarea compleja: ")

    async def decompose_task(self, task: str) -> List[str]:
        prompt = f"Descompone la siguiente tarea compleja en una lista de subtareas más pequeñas: {task}"
        response = await self.agent.send_message(None, prompt)
        if response and 'content' in response:
            subtasks = response['content'][0].text.split('\n')
            return [subtask.strip() for subtask in subtasks if subtask.strip()]
        return []

    async def execute_subtask(self, subtask: str) -> str:
        prompt = f"Ejecuta la siguiente subtarea y proporciona una respuesta detallada: {subtask}"
        response = await self.agent.send_message(None, prompt)
        if response and 'content' in response:
            return response['content'][0].text
        return "No se pudo completar la subtarea."

    async def run(self):
        self.welcome()
        while True:
            self.show_menu()
            choice = await self.get_user_input()
            
            if choice == '1':
                task = await self.get_complex_task()
                subtasks = await self.decompose_task(task)
                print("\nTarea descompuesta en las siguientes subtareas:")
                for i, subtask in enumerate(subtasks, 1):
                    print(f"{i}. {subtask}")
                
                print("\nEjecutando subtareas:")
                for i, subtask in enumerate(subtasks, 1):
                    print(f"\nEjecutando subtarea {i}: {subtask}")
                    result = await self.execute_subtask(subtask)
                    print(f"Resultado: {result}")
                
                print("\nTarea compleja completada.")
            
            elif choice == '2':
                print("Gracias por usar el Asistente de Tareas Complejas. ¡Hasta luego!")
                break
            
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

async def main():
    ui = UserInterface()
    await ui.run()

if __name__ == "__main__":
    asyncio.run(main())
