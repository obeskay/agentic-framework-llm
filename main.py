import colorama
from agents.self_improvement_agent import SelfImprovementAgent

def main():
    colorama.init()
    agent = SelfImprovementAgent()
    print(colorama.Fore.GREEN + "Starting code analysis...")
    agent.analyze_codebase()
    print(colorama.Fore.BLUE + "Proposing improvements...")
    agent.propose_improvements()
    print(colorama.Fore.MAGENTA + "Applying improvements...")
    agent.apply_improvements()
    print(colorama.Fore.RESET + "Improvements applied successfully.")

if __name__ == "__main__":
    main()
