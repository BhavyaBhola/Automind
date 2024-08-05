def generate_initial_prompt(question, actions, backstory):
    prompt = f"""
    You are a helpful assistant with access to the following actions:

    Available actions , Choose the most relevant action(s) to answer users query:
    {[action.get_tool_info() for action in actions]}

    You have the following backstory:
    {backstory}

    To assist with the user's request, provide a single response in the following format:

    <output>
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
    </output>

    Follow the given examples:
    --Query:
    What is the capital of France?
    <output>
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
    </output>


    Guidelines:
    1. If no action matches the user's request, respond politely that you cannot help.
    2. Ensure the action call is complete and correctly formatted.
    3. Provide a single, precise answer; avoid repetition.
    4. Replace <relevant_action_name> with the name of the action being used.
    5. Only provide a single JSON output response, and ensure it's enclosed within <output></output> delimiters.

    -- User Query:
    {question}
    """
    return prompt
