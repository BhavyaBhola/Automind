# Automind

Automind is an autonomous agent library designed for performing various tasks such as information retrieval and complex decision-making using large language models (LLMs). Automind provides easy-to-use, configurable agents that can be customized with different tools and LLMs.

## Installation

To install Automind, you need to clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone https://github.com/yourusername/automind.git

# Navigate to the directory
cd automind

# Install the required dependencies
pip install -r requirements.txt
```

Make sure you have Python 3.8 or later installed in your environment.

## Usage

Automind provides different types of agents for handling various types of tasks. Below are some examples to help you get started:

### SingleAgent

The `SingleAgent` is useful for simpler tasks like information retrieval.

![SingleAgent](https://github.com/BhavyaBhola/Automind/blob/main/img/single%20agent.png)

**Example Usage:**

```python
from automind.agents.SingleAgent import SingleAgent
from automind.actions.tools.duckduckgosearch import DuckDuckGoSearch
from automind.actions.tools.wikisearch import WikiSearch
from automind.llms.gemini import Gemini_model

def main():
    configs = {
        "google_api_key": "<Your_api_key>",
        "temperature": 0.4
    }

    llm = Gemini_model(gemini_model_name="gemini-1.5-flash", configs=configs)

    test_exe = SingleAgent(
        question="Latest Geopolitical News",
        llm=llm,
        summary=True,
        actions=[DuckDuckGoSearch, WikiSearch],
        backstory='You are an expert researcher who is able to extract the relevant information'
    )
    res = test_exe.run()
    print(res)

if __name__ == '__main__':
    main()
```

### ThinkAgent

The `ThinkAgent` uses the reaction and action paradigm and is useful for more complex tasks requiring multiple iterations.

![ThinkAgent](https://github.com/BhavyaBhola/Automind/blob/main/img/think%20agent.png)

**Example Usage:**

```python
from automind.agents.ThinkAgent import ThinkAgent
from automind.actions.tools.duckduckgosearch import DuckDuckGoSearch
from automind.actions.tools.wikisearch import WikiSearch
from automind.llms.gemini import Gemini_model

def main():
    configs = {
        "google_api_key": "<Your_api_key>",
        "temperature": 0.4
    }

    llm = Gemini_model(gemini_model_name="gemini-1.5-flash", configs=configs)

    test_exe = ThinkAgent(
        question="Plan a detailed 3 day trip to Rajasthan, India",
        llm=llm,
        num_iterations=2,
        actions=[DuckDuckGoSearch, WikiSearch],
        backstory='You are an expert researcher who is able to extract the relevant information'
    )
    res = test_exe.run()
    print(res)

if __name__ == '__main__':
    main()
```

## Creating Custom Action Tools

You can create your own custom action tools in Automind by inheriting from the `BaseAction` class and implementing the `execute` method.

### Example of Creating a Custom Action Tool

To create a custom action tool, you need to inherit from `BaseAction` and implement the `execute` method:

```python
from automind.actions.base import BaseAction

class CustomAction(BaseAction):

    def execute(self):
        # Custom logic for the action
        result = "Executed custom action."
        return result
```

This allows you to extend the capabilities of Automind by defining your own tools that perform specific actions based on your requirements.

## Contributing

Feel free to fork this repository and make contributions. Please ensure your pull requests adhere to the project's coding standards.