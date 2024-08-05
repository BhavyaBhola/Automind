from pydantic import BaseModel
from typing import Any
from abc import abstractmethod

class BaseLLM(BaseModel):
    """
    A base class for language models, providing a standard interface for building
    and running models.

    Attributes:
        configs (Any): Configuration settings for the model.
        model (Any): The actual language model instance, initialized to None by default.
    """

    configs: Any
    model: Any = None

    @abstractmethod
    def build(self):
        """
        Abstract method to build and initialize the language model.
        Implementations should define how the model is constructed and configured.
        """
        pass

    @abstractmethod
    def run(self, prompt: str):
        """
        Abstract method to run the language model with a given prompt.
        Implementations should define how the model processes the prompt and generates a response.

        Args:
            prompt (str): The input text prompt to be processed by the model.
        """
        pass
