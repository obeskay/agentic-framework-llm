from agents.self_improvement_agent import SelfImprovementAgent

def main():
    agent = SelfImprovementAgent()
    agent.analyze_codebase()
    agent.propose_improvements()
    agent.apply_improvements()

if __name__ == "__main__":
    main()
