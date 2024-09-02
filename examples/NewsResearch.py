from automind.agents.SingleAgent import SingleAgent
from automind.actions.tools.duckduckgosearch import DuckDuckGoSearch
from automind.actions.tools.wikisearch import WikiSearch
from automind.llms.gemini import Gemini_model



def main():
    configs = {
    "google_api_key":"<Your_api_key>",
    "temperature":0.4
    }

    llm = Gemini_model(gemini_model_name="gemini-1.5-flash" , configs=configs)

    test_exe = SingleAgent(question="Latest Geopolitical News",
                            llm=llm ,
                            summary=True,
                            actions=[DuckDuckGoSearch,WikiSearch],
                            backstory='You are an expert researcher who is able to extract the relevant information'
                            )
    res = test_exe.run()

if __name__=='__main__':
    main()



#output -->

"""
- **Title:** Geopolitics Politics, Relations & Current Affairs - Foreign Policy
- **Link:** https://foreignpolicy.com/tag/geopolitics/
- **Summary:**  Provides weekly news, analysis, and data on geopolitical developments, including a focus on the shift in power dynamics between Europe and Asia. 

- **Title:** Geopolitics - Financial Times
- **Link:** https://www.ft.com/geopolitics
- **Summary:** Offers comprehensive coverage of global geopolitical developments, including news, analysis, and opinion on politics and international relations.

"""