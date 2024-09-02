from automind.agents.ThinkAgent import ThinkAgent
from automind.actions.tools.duckduckgosearch import DuckDuckGoSearch
from automind.actions.tools.wikisearch import WikiSearch
from automind.llms.gemini import Gemini_model


def main():
    configs = {
        "google_api_key":"<your_api_key",
        "temperature":0.4
    }

    llm = Gemini_model(gemini_model_name="gemini-1.5-flash" , configs=configs)

    test_exe = ThinkAgent(question="Plan a detailed 3 day trip to Rajasthan,India",
                            llm=llm ,
                            num_iterations=2,
                            actions=[DuckDuckGoSearch,WikiSearch],
                            backstory='You are an expert researcher who is able to extract the relevant information'
                            )
    res = test_exe.run()

if __name__=='__main__':
    main()



# output -->
"""

==============================
🎯 Final Answer:
 Based on my research, a 3-day trip to Rajasthan could include:
Day 1: Arrive in Jaipur, the capital city, and explore the iconic Amber Fort, Hawa Mahal (Palace of Winds), and the City Palace. Stay overnight in a heritage hotel for a truly authentic experience.
Day 2: Take a day trip to the beautiful city of Udaipur, known as the "Venice of the East". Visit the City Palace, Lake Pichola, and Jag Mandir. Enjoy a boat ride on the lake and stay overnight in a lakeside resort.
Day 3: Travel to Jodhpur, the "Blue City", and explore the Mehrangarh Fort, Jaswant Thada, and the bustling markets. Stay overnight in a traditional haveli (mansion) for a unique cultural experience.

Transportation: 
- You can travel between cities by train, bus, or car. 
- For shorter distances, consider using taxis, auto-rickshaws, or even camels.

Accommodation:
- Rajasthan offers a wide range of accommodation options, from budget-friendly guesthouses and homestays to luxurious palaces and forts. 
- Heritage hotels and havelis are popular choices for their unique charm and historical significance.

Remember to book your accommodation and transportation in advance, especially during peak season. Enjoy your trip to Rajasthan! 

==============================


"""