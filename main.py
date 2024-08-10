import colorama
from agents.self_improvement_agent import SelfImprovementAgent
from tools.write_file import write_file
from tools.read_file import read_file
from tools.search_and_replace import search_and_replace
from tools.tool_schema_converter import convert_tools_to_openai_schema

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

    # Convert tools to OpenAI schema
    tools = convert_tools_to_openai_schema()
    
    # Example usage of the tools
    file_path = 'example.txt'
    content = 'Hello, World!'
    write_file(file_path, content)
    print(f"File written with content: {content}")

    read_content = read_file(file_path)
    print(f"File read content: {read_content}")

    search_and_replace(file_path, 'World', 'OpenAI')
    updated_content = read_file(file_path)
    print(f"File updated content: {updated_content}")

if __name__ == "__main__":
    main()
