from automind.llms.base import BaseLLM
from langchain_community.llms import VLLM

class AnyhfLLM(BaseLLM):
    """
    A class for handling Hugging Face language models, inheriting from BaseLLM.
    
    Attributes:
        hf_model_name (str): The name of the Hugging Face model to be used.
    """

    hf_model_name: str

    def build(self):
        """
        Builds and initializes the Hugging Face language model using the provided configurations.

        Returns:
            VLLM: The initialized language model instance.
        """
        self.model = VLLM(
            model=self.hf_model_name,
            trust_remote_code=True,  # mandatory for HF models
            max_new_tokens=self.configs.get("max_new_tokens"),
            top_k=self.configs.get("top_k"),
            top_p=self.configs.get("top_p"),
            temperature=self.configs.get("temperature"),
            repetition_penalty=self.configs.get("repetition_penalty"),
            dtype=self.configs.get("dtype"),
            vllm_kwargs=self.configs.get("vllm_kwargs")
        )

        return self.model

    def run(self, prompt: str):
        """
        Runs the language model with a given prompt. Builds the model if it is not already built.

        Args:
            prompt (str): The input text prompt to be processed by the model.

        Returns:
            str: The generated response from the model.
        """
        if not self.model:
            self.build()
        return self.model.invoke(prompt)



'''
Example configs:

configs = {
    "max_new_tokens": 512,
    "top_k": 2,
    "top_p": 0.95,
    "temperature": 0.8,
    "repetition_penalty": 1.1,
    "dtype": "float16",
    "vllm_kwargs": {                      # add None if quantized models are not used
        "quantization": "awq"
    }
}

'''