import random
import json
import requests


# Hard coded rn, switch later
# level_prompt = "You are an elementary school teacher who wants to teach her students about household objects. You need to verify, in a one word answer of yes or no, whether these objects fulfill the object category that was selected."
# user_prompt = "car"

def response_trial(level_prompt, user_prompt):
    stream = False
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": "sk-tune-zcDc8BfUPx1EG2FycwJc5GxX3bZjiDr8Izc",
        "Content-Type": "application/json",
    }
    data = {
    "temperature": 0.9,
        "messages":  [
        {
            "role": "system",
            "content": f"{level_prompt}"
        },
        {
            "role": "user",
            "content": f"{user_prompt}"
        }
        ],
        "model": "meta/llama-3.1-70b-instruct",
        "stream": stream,
        "frequency_penalty":  0.2,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    print(level_prompt)
    print(user_prompt)
    print(response.json())
    trial = response.json()["choices"][0]["message"]["content"]
    print("Trial output: ", trial)
    return trial
    

def binary_response_prompt(level_prompt: str, user_prompt: str) -> bool:
    data = {}
    data['level_prompt'] = level_prompt
    data['user_prompt'] = user_prompt
    answer = response_trial(level_prompt,user_prompt)
    print(answer)
    data['binary_response'] = True if answer == "Yes" else False
    
    if data['binary_response'] == "error":
        raise ValueError("Error: Invalid query")

    return data

# if __name__ == "__main__": 
    # response_trial(level_prompt,user_prompt)
    # response_trial(level_prompt,user_prompt="Flowerpot")

# sk-tune-zcDc8BfUPx1EG2FycwJc5GxX3bZjiDr8Izc