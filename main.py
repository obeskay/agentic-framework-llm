import asyncio
from user_interface import UserInterface

async def main():
    ui = UserInterface()
    await ui.run()

if __name__ == "__main__":
    asyncio.run(main())
