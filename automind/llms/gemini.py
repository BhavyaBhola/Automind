from automind.llms.base import BaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI

class Gemini_model(BaseLLM):

    gemini_model_name:str

    def build(self):
        self.model = ChatGoogleGenerativeAI(
                  google_api_key = self.configs.get("google_api_key"),
                  model=self.gemini_model_name,
                  temperature=self.configs.get("temperature")
              )

        return self.model
    
    def run(self,prompt):

        if not self.model:
            self.build()
        resp = self.model.invoke(prompt)
        return resp.content