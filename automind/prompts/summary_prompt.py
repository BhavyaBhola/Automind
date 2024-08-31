def summary_prompt(response):
    prompt = f"""
    You are an expert at summarizing information concisely and clearly. Summarize the following output into bullet points, providing only the title, link, and a brief summary of the body for each item. 
    Do not include any additional text and provide explanations—only the bullet points.

    {response}
    """
    return prompt
