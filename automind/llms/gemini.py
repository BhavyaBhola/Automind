from automind.llms.base import BaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini_model(BaseLLM):
    """
    A class that wraps around the Google Generative AI model for use in the Automind framework.
    
    Attributes:
        gemini_model_name (str): The name of the Gemini model to use.
    """
    
    gemini_model_name: str

    def build(self):
        """
        Initializes the Google Generative AI model using the provided configuration.

        Returns:
            ChatGoogleGenerativeAI: The initialized Google Generative AI model instance.
        """
        self.model = ChatGoogleGenerativeAI(
            google_api_key=self.configs.get("google_api_key"),
            model=self.gemini_model_name,
            temperature=self.configs.get("temperature")
        )

        return self.model
    
    def run(self, prompt: str) -> str:
        """
        Runs the model with the given prompt and returns the response content.

        Args:
            prompt (str): The input prompt to send to the model.

        Returns:
            str: The response content from the model.
        """
        if not self.model:
            self.build()
        resp = self.model.invoke(prompt)
        return resp.content
