from typing import Any
import importlib
import json
import re
from automind.agents.base import BaseLLM
from automind.prompts.thinking_prompt import generate_thinking_prompt

def extract_thought(text: str) -> Any:
    """
    Extracts the 'Thought' section from a given string.

    Args:
        text (str): The text containing the 'Thought' section.

    Returns:
        str or None: The extracted 'Thought' text if found, otherwise None.
    """
    thought_match = re.search(r'Thought: (.*?)(?=Action:)', text, re.DOTALL)
    thought = thought_match.group(1).strip() if thought_match else None
    return thought

def extract_action(text: str) -> Any:
    """
    Extracts the 'Action' section from a given string formatted as JSON within markdown-style code blocks.

    Args:
        text (str): The text containing the 'Action' section.

    Returns:
        str or None: The extracted 'Action' text if found, otherwise None.
    """
    action_match = re.search(r'Action:\n(```json\n.*?\n```)', text, re.DOTALL)
    
    if action_match:
        return f"Action:\n{action_match.group(1)}"
    else:
        return None

def extract_final_answer(text: str) -> Any:
    """
    Extracts the 'Final Answer' section from a given string.

    Args:
        text (str): The text containing the 'Final Answer' section.

    Returns:
        str or None: The extracted 'Final Answer' text if found, otherwise None.
    """
    pattern = r"Final Answer:([\s\S]*)"
    match = re.search(pattern, text)

    if match:
        final_answer = match.group(1)
        return final_answer
    else:
        return None

def extract_output(content: str) -> Any:
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
    """
    An agent that uses a language learning model (LLM) to think, perform actions, and generate responses iteratively.

    This class extends the BaseLLM class to provide functionality for generating prompts, running tasks, and
    iterating through steps to refine the output of the LLM.

    Attributes:
        agent_scratchpad (str): A buffer to keep track of the thought process, actions, and observations.
    """
    agent_scratchpad: str = ""

    def generate_prompt(self):
        """
        Generates a prompt for the LLM using the given question, actions, backstory, and current agent state.

        Returns:
            str: The generated prompt for the LLM.
        """
        return generate_thinking_prompt(question=self.question, actions=self.actions, backstory=self.backstory, agent_scratchpad=self.agent_scratchpad)

    def run_task(self):
        """
        Executes the task by iterating through a sequence of thoughts and actions until the desired number of iterations is reached.

        During each iteration, it generates a prompt, invokes the LLM to obtain a response, extracts the thought and action,
        performs the action, observes the result, and updates the agent's scratchpad.

        Returns:
            Any: The final answer extracted from the LLM's response.
        """
        steps = 1
        while steps <= self.num_iterations:
            print(f"\n{'-'*30}\nIteration: {steps}\n{'-'*30}")
            print("🤔 Thinking...\n")
            
            llm_response = self.llm.run(self.generate_prompt())
            thought = extract_thought(llm_response)
            print(f"💡 Thought:\n{thought}\n")

            action = extract_action(llm_response)
            action_response = extract_output(action)
            cls_name = action_response['name']
            print(f"🛠️ Action being used: {cls_name}\n")

            mod_name = action_response['arguments']['module']
            tool_cls = getattr(importlib.import_module(mod_name), cls_name)
            tool_cls = tool_cls(query=action_response['arguments']['query'])
            setattr(tool_cls, 'llm', self.llm)
            tool_obj = tool_cls.execute()
            observation = tool_obj

            print(f"👁️ Observation:\n{observation}\n")

            # Update the scratchpad with thought, action, and observation
            self.agent_scratchpad += f"Thought: {thought}\n"
            self.agent_scratchpad += f"Action: {action}\n"
            self.agent_scratchpad += f"Observation: {observation}\n"
            
            steps += 1 
            
        final_answer = extract_final_answer(llm_response)
        print(f"\n{'='*30}\n🎯 Final Answer:\n{final_answer}\n{'='*30}")
        return final_answer

    def run(self):
        """
        Runs the agent's task execution process.

        This method calls the `run_task` method to perform the sequence of actions and obtain the final answer.

        Returns:
            Any: The result from running the task.
        """
        return self.run_task()
