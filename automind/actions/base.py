from pydantic import BaseModel
from abc import abstractmethod
from typing import Any , get_type_hints
from textwrap import dedent
import json


class BaseAction(BaseModel):
    """
    A base class for defining actions that can be executed. This class is meant to be inherited by other classes
    that implement the `execute` method.
    """

    llm: Any = None

    @abstractmethod
    def execute(self):
        """
        An abstract method that must be implemented by any subclass. This method defines the action to be executed.
        """
        pass

    @classmethod
    def get_tool_info(cls):
        """
        A class method that returns information about the tool (class) and its parameters in JSON format.

        Returns:
            str: A JSON-formatted string containing the class name, class docstring, parameter names and their 
            descriptions (excluding those in `expel_types`), and the return type of the `execute` method.
        """
        type_hints = get_type_hints(cls.execute)
        expel_types = ['llm']
        tool_info = {
            "cls": {
                "kls": cls.__name__,
                "doc": dedent(cls.__doc__).strip() if cls.__doc__ else "",
            },
            "params": {
                field_name: field.description
                for field_name, field in cls.model_fields.items()
                if field_name not in expel_types
            },
            "returns": type_hints.get('return', 'void').__name__
        }

        return json.dumps(tool_info, indent=2)
