from pydantic import BaseModel
from typing import Any , Optional
from abc import abstractmethod

class BaseLLM(BaseModel):
    """
    Base class for a Language Learning Model (LLM) agent framework.

    This class defines the structure for an LLM-based agent that can perform tasks using a given set of actions and tools.
    It provides an abstract interface for generating prompts, running tasks, and executing the entire process.

    Attributes:
        question (str): The question or input prompt for the LLM.
        llm (Any): The LLM model to be used for generating responses.
        actions (Any): The available actions or tools that the LLM can use to complete a task.
        num_iterations (int): The number of iterations the agent should run to refine the output.
        backstory (str): An optional backstory or context that provides additional information to the LLM.
    """

    question: str
    llm: Any
    actions: Any
    num_iterations: Optional[int]
    backstory: str

    @abstractmethod
    def generate_prompt(self):
        """
        Abstract method to generate a prompt for the LLM.

        This method should be implemented by subclasses to create a prompt that incorporates
        the question, actions, backstory, and other necessary context.
        """
        pass

    @abstractmethod
    def run_task(self):
        """
        Abstract method to execute a task using the LLM.

        This method should be implemented by subclasses to define the logic for running a specific task
        using the LLM and available actions.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Abstract method to run the entire process for the LLM agent.

        This method should be implemented by subclasses to define the workflow for generating the prompt,
        executing tasks, and iterating to refine the results.
        """
        pass
