def generate_thinking_prompt(question , actions , backstory , agent_scratchpad):
    prompt = f"""
      You are a helpful assistant with the following backstory
      {backstory}

      answer the following questions as best you can. 
      {question}

      You have access to the following tools:
      {[action.get_tool_info() for action in actions]}

      The way you use the tools is by specifying a json blob.
      Specifically, this json should have a `action` key (with the name of the tool to use) and a `action_input` key (with the input to the tool going here).

      The only values that should be in the "name" field are: {[action.__name__ for action in actions]}

      The $JSON_BLOB should only contain a SINGLE action, do NOT return a list of multiple actions. Here is an example of a valid $JSON_BLOB:

      ```json
      {{
        "name": "<relevant_action_name>",
        "arguments": {{
            "query": "<query_from_user>",
            "type": "<data_type_of_query>",
            "module":"<module_name>"
        }}
    }}
      ```

      Example of $JSON_BLOB:
      ```json
    {{
        "name": "WikiSearch",
        "arguments": {{
            "query": "What is capital of France",
            "type": "str",
            "module":"automind.actions.tools.wikisearch"
        }}
    }}
    ```

      ALWAYS use the following format:

      Question: the input question you must answer
      Thought: you should always think about what to do
      Action:
      $JSON_BLOB
      Observation: the result of the action
      ... (this Thought/Action/Observation can repeat N times)
      Thought: I now know the final answer
      Final Answer: the final answer to the original input question
      Begin! Reminder to always use the exact characters `Final Answer` when responding.

      This is your previous work:
      {agent_scratchpad}

    """
    return prompt