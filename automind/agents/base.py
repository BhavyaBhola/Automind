from pydantic import BaseModel
from typing import Any
from abc import abstractmethod

class BaseLLM(BaseModel):
    question:str
    llm:Any
    actions:Any
    num_iterations:int
    backstory:str
    
    @abstractmethod
    def generate_prompt(self):
        pass

    @abstractmethod
    def run_task(self):
        pass

    @abstractmethod
    def run(self):
        pass

