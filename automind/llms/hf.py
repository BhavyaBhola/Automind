from automind.llms.base import BaseLLM
from langchain_huggingface import HuggingFacePipeline

class AnyhfLLM(BaseLLM):
    """
    AnyhfLLM is a custom implementation of the BaseLLM class designed to work 
    with Hugging Face models using the HuggingFacePipeline.

    Attributes:
        hf_model_name (str): The name of the Hugging Face model to be used.
    """

    hf_model_name: str

    def build(self):
        """
        Builds and initializes the Hugging Face model pipeline with the specified model ID 
        and configurations.

        Returns:
            HuggingFacePipeline: An initialized Hugging Face model pipeline.
        """
        self.model = HuggingFacePipeline.from_model_id(
            model_id=self.hf_model_name, 
            task="text-generation",
            device=0,
            pipeline_kwargs={
                "temperature": self.configs.get("temperature"),
                "max_new_tokens": self.configs.get("max_new_tokens"),
                "top_k": self.configs.get("top_k"),
                "top_p": self.configs.get("top_p"),
                "repetition_penalty": self.configs.get("repetition_penalty")
            }
        )
        
        return self.model

    def run(self, prompt):
        """
        Runs the model pipeline to generate text based on the provided prompt.

        Args:
            prompt (str): The input prompt for the model to generate text from.

        Returns:
            str: The generated text response from the model.
        """
        if not self.model:
            self.build()
        resp = self.model.invoke(prompt)
        return resp
