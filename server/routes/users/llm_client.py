import random

def binary_response_prompt(level_prompt: str, user_answer: str) -> bool:
    data = {}
    data['level_prompt'] = level_prompt
    data['user_answer'] = user_answer
    data['binary_response'] = random.choice([True, False, "error"])
    
    if data['binary_response'] == "error":
        raise ValueError("Error: Invalid query")

    return data