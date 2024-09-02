from pydantic import BaseModel
from typing import Any
from automind.prompts.initial_prompt import generate_initial_prompt
from automind.prompts.summary_prompt import summary_prompt
from automind.agents.base import BaseLLM
import importlib
import json
import re


def extract_output(content: str):
    """
    Extracts JSON content from a string enclosed in markdown-style code blocks.

    Args:
        content (str): The string containing JSON data within markdown code blocks.

    Returns:
        dict or None: The parsed JSON data if found, otherwise None.
    """
    json_patters = r"```json(.*?)```"
    matches = re.search(json_patters, content, re.DOTALL)
    if not matches:
        return None

    json_content = matches.group(1)
    json_data = json.loads(json_content)
    return json_data


class SingleAgent(BaseLLM):
    """
    SingleAgent represents a single agent in a task execution system.

    Attributes:
        question (str): The initial question or task for the agent.
        llm (Any): The language model to be used for processing.
        actions (Any): The available actions the agent can perform.
        num_iterations (int): The number of iterations the agent will perform.
        backstory (str): The backstory or context for the task.

    Methods:
        generate_prompt(): Generates the initial prompt for the language model.
        run_task(): Executes the task by interacting with the language model and tools.
        run(): Runs the task execution.
    """

    summary:bool
    num_iterations:int = None

    def generate_prompt(self):
        """
        Generates the initial prompt using the provided question, actions, and backstory.

        Returns:
            str: The generated prompt string.
        """
        return generate_initial_prompt(question=self.question, actions=self.actions, backstory=self.backstory)

    def run_task(self):
        """
        Runs the task by interacting with the language model, executing the appropriate tool,
        and returning the tool's response.

        Returns:
            dict: The response containing the tool name and its execution result.
        """
        llm_response = self.llm.run(self.generate_prompt())
        llm_response = extract_output(llm_response)

        cls_name = llm_response['name']
        mod_name = llm_response['arguments']['module']
        
        print(f"\n{'-' * 30}\n📦 Loading Tool: {cls_name} from module: {mod_name}\n{'-' * 30}")
        tool_cls = getattr(importlib.import_module(mod_name), cls_name)
        tool_cls = tool_cls(query=llm_response['arguments']['query'])
        setattr(tool_cls, 'llm', self.llm)
        
        print(f"\n{'-' * 30}\n🚀 Executing Tool: {cls_name}...\n{'-' * 30}")
        tool_obj = tool_cls.execute()

        print(f"\n{'-' * 30}\n🛠️ Tool Execution Completed.\n{'-' * 30}")
        print(f"Tool Name: {cls_name}\nTool Response: {tool_obj}\n")

        response = {
            "tool_name": cls_name,
            "tool_response": tool_obj
        }

        if self.summary:
            print(f"\n{'-' * 30}\n📝 Generating Summary...\n{'-' * 30}")
            response = self.llm.run(summary_prompt(tool_obj))
            print(f"\n{'-' * 30}\n📄 Summary Generated:\n{'-' * 30}")
            print(f"{response}\n")
            return response
        
        print(print(f"\n{'='*30}\n🎯 Final Answer:\n{response}\n{'='*30}"))
        return response


    def run(self):
        """
        Executes the agent's task by calling the run_task method.

        Returns:
            dict: The final response from the task execution.
        """
        return self.run_task()
