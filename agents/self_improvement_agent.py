import os
import inspect
import pylint.lint
import flake8.api.legacy as flake8
from .base_agent import BaseAgent

class SelfImprovementAgent(BaseAgent):
    def analyze_codebase(self):
        # Enhanced static analysis of the codebase
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.issues = {}  # Dictionary to store identified issues and proposed fixes
        files = os.popen('git ls-files --exclude-standard --others --cached').read().splitlines()
        for file_path in files:
            if file_path.endswith(".py"):
                print(f"Analyzing {file_path}...")
                # Perform more detailed analysis
                self._detailed_analysis(file_path)

    def _detailed_analysis(self, file_path):
        # Detailed analysis logic using pylint and flake8
        pylint_results = pylint.lint.Run([file_path], do_exit=False)
        flake8_results = flake8.get_style_guide().check_files([file_path])
        self.issues.extend([message for message in pylint_results.linter.stats.global_note])
        self.issues.extend(flake8_results.get_statistics('E'))

    def propose_improvements(self):
        # Propose improvements based on detailed analysis
        print("Proposing improvements based on detailed analysis...")
        for issue in self.issues:
            # Generate a proposed fix for the issue
            fix = self._generate_fix(issue)
            self.issues[issue] = fix
            print(f"Proposed improvement: {issue} - Fix: {fix}")

    def apply_improvements(self):
        # Automate the application of proposed improvements
        print("Applying proposed improvements...")
        for issue, fix in self.issues.items():
            # Apply the fix safely
            if self._apply_fix(issue, fix):
                print(f"Applied fix for {issue}")
            else:
                print(f"Failed to apply fix for {issue}")

    def _apply_fix(self, issue, fix):
        # Safely apply the fix without breaking the codebase
        try:
            file_path = issue.split(" ")[-1]
            with open(file_path, 'r') as f:
                content = f.read()
            # Apply the fix
            content = content.replace(fix['search'], fix['replace'])
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error applying fix: {e}")
            return False

    def _generate_fix(self, issue):
        # Generate a proposed fix for the issue
        # This is a placeholder and should be replaced with actual logic
        if "Unused imports" in issue:
            file_path = issue.split(" ")[-1]
            with open(file_path, 'r') as f:
                content = f.read()
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "import" in line:
                    return {'search': line, 'replace': "# " + line}
        return {}
import os
import ast
import astroid
import asyncio
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class SelfImprovementAgent(BaseAgent):
    def __init__(self, model: str = "gpt-4o-mini"):
        super().__init__(model)
        self.issues: Dict[str, List[Dict[str, Any]]] = {}

    async def analyze_codebase(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files = os.popen('git ls-files --exclude-standard --others --cached').read().splitlines()
        tasks = [self._detailed_analysis(file_path) for file_path in files if file_path.endswith(".py")]
        await asyncio.gather(*tasks)

    async def _detailed_analysis(self, file_path: str) -> None:
        try:
            print(f"Analyzing {file_path}...")
            async with asyncio.timeout(30):  # Límite de 30 segundos por archivo
                with open(file_path, 'r') as file:
                    code = file.read()
                
                # Análisis estático con ast
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if len(node.body) > 20:
                            self._add_issue(file_path, f"Function '{node.name}' is too long (> 20 lines)")

                # Análisis con astroid
                module = astroid.parse(code)
                for function in module.body:
                    if isinstance(function, astroid.FunctionDef):
                        complexity = function.complexity()
                        if complexity > 10:
                            self._add_issue(file_path, f"Function '{function.name}' has high complexity ({complexity})")

        except asyncio.TimeoutError:
            print(f"Analysis of {file_path} timed out after 30 seconds")
        except Exception as e:
            print(f"Error analyzing {file_path}: {str(e)}")

    def _add_issue(self, file_path: str, issue: str) -> None:
        if file_path not in self.issues:
            self.issues[file_path] = []
        self.issues[file_path].append({"description": issue, "fix": None})

    async def _apply_fix(self, file_path: str, issue: Dict[str, Any]) -> bool:
        if not issue['fix']:
            return False
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            content = content.replace(issue['fix']['search'], issue['fix']['replace'])
            with open(file_path, 'w') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error applying fix to {file_path}: {str(e)}")
            return False

    async def _generate_fix(self, file_path: str, issue: Dict[str, Any]) -> Dict[str, str]:
        prompt = f"Generate a fix for the following issue in {file_path}: {issue['description']}"
        response = await self.send_message(None, prompt)
        if response and 'content' in response:
            fix_suggestion = response['content'][0].text
            return {"search": issue['description'], "replace": fix_suggestion}
        return {}

    async def generate_new_tool(self, description: str) -> str:
        prompt = f"Generate Python code for a new tool with the following description: {description}"
        response = await self.send_message(None, prompt)
        if response and 'content' in response:
            return response['content'][0].text
        return ""

    async def improve_codebase(self) -> None:
        await self.analyze_codebase()
        for file_path, issues in self.issues.items():
            for issue in issues:
                if not issue['fix']:
                    issue['fix'] = await self._generate_fix(file_path, issue)
                if issue['fix']:
                    success = await self._apply_fix(file_path, issue)
                    if success:
                        print(f"Applied fix for {issue['description']} in {file_path}")
                    else:
                        print(f"Failed to apply fix for {issue['description']} in {file_path}")
