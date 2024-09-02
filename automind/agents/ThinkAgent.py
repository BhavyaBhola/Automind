from typing import Any
import importlib
import json
import re
from automind.agents.base import BaseLLM
from automind.prompts.thinking_prompt import generate_thinking_prompt


def extract_thought(text):
    thought_match = re.search(r'Thought: (.*?)(?=Action:)', text, re.DOTALL)
    thought = thought_match.group(1).strip() if thought_match else None
    return thought

def extract_action(text):
    action_match = re.search(r'Action:\n(```json\n.*?\n```)', text, re.DOTALL)
    
    if action_match:
        return f"Action:\n{action_match.group(1)}"
    else:
        return None

def extract_final_answer(text):
    pattern = r"Final Answer:([\s\S]*)"
    match = re.search(pattern, text)

    if match:
        final_answer = match.group(1)
        return final_answer
    else:
        return None


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


class ThinkAgent(BaseLLM):

    agent_scratchpad:str = ""

    def generate_prompt(self):
        return generate_thinking_prompt(question=self.question , actions=self.actions , backstory=self.backstory , agent_scratchpad=self.agent_scratchpad)

    def run_task(self):
        steps=1
        while steps<=self.num_iterations:
            
            print(f"{steps} iteration \n")
            print("Thinking...\n")
            llm_response = self.llm.run(self.generate_prompt())
            thought = extract_thought(llm_response)
            print(f"Thought:{thought}\n")
            action = extract_action(llm_response)
            action_response = extract_output(action)
            cls_name = action_response['name']
            print(f"Action being used:{cls_name}\n")
            mod_name = action_response['arguments']['module']
            tool_cls = getattr(importlib.import_module(mod_name),cls_name)
            tool_cls = tool_cls(query=action_response['arguments']['query'])
            setattr(tool_cls , 'llm' , self.llm)
            tool_obj = tool_cls.execute()
            observation = tool_obj

            self.agent_scratchpad += f"Thought: {thought}\n"
            self.agent_scratchpad += f"Action: {action}\n"
            self.agent_scratchpad += f"Observation: {observation}\n"
            
            steps+=1 
        return extract_final_answer(llm_response)

    def run(self):
        return self.run_task()