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
    # print(level_prompt)
    # print(user_prompt)
    # print(response.json())
    trial = response.json()["choices"][0]["message"]["content"]
    # print("Trial output: ", trial)
    return trial
    

def binary_response_prompt(level_prompt: str, user_prompt: str) -> bool:
    data = {}
    system_prompt = "You are a yes or no machine. You must answer with a single word, either 'Yes' if your "
    system_prompt += " response is affirmative or 'No' if your response is negative. The user will propose an answer and you will " 
    system_prompt += "decide if the user's answer is a correct response to the question. You must respond in exactly ONE word. If "
    system_prompt += "you respond with any more than the word 'Yes' or the word 'No', your response will be invalid and our system will break "
    system_prompt += "The question is: " + level_prompt
    answer = response_trial(system_prompt, user_prompt)
    print(answer)
    data['binary_response'] = True if answer == "Yes" else False
    
    if data['binary_response'] == "error":
        raise ValueError("Error: Invalid query")

    return data

def llm_classify_object(user_prompt: str):
    level_prompt = "You are an elementary school english teacher. "
    level_prompt += "Your students are playing a game in which they are placed in different puzzle situations and attempt to "
    level_prompt += "solve them using any idea they can think of.  Students will enter a word and you will act as a classifer, deciding "
    level_prompt += "whether the student's idea fits into the categories of a fluid, an inanimate solid, a living creature, or none of the above. "
    level_prompt += "Your response should strictly be a list of comma separated key pair values, depending on which classification you have decided, "
    level_prompt += "using the following format to estimate certain parameters. 'Type: (fluid, inanimate solid, life, or none) "
    level_prompt += "if a student's answer doesn't fit well into any of the categories, or is not appropriate for elementary school children, "
    level_prompt += "return a type of none. For all non-none types, also add the following parameters: color: hex_string (ex. #FFFFFF), "
    level_prompt += "sub_color: hex_string (ex. #000000), size: string (one of 'wide', 'tall', 'small', or 'big'), viscosity for all fluid objects: a "
    level_prompt += "floating point between 0 and 1 with 1 being very viscous and 0 being not viscous at all, dynamic: a floating point"
    level_prompt += "number between 0 and 1 describing how expressive the word is. Inanimate solids should additionally have physics_type: "
    level_prompt += "'movable' or 'rigid' defining if this object can move (for example brick or stone are rigid, but bottles and pans are immovable) "
    level_prompt += "Finally, living objects should include movement_type: string (one of 'land', 'air', 'fluid'), activity: floating point "
    level_prompt += "from 0 to 1 representing how fast this creature moves. Please strictly respond with the comma seperated list format, with no "
    level_prompt += "additional information or punctuation. If you can not perform the task, respond with the none type. We're working with children, "
    level_prompt += " so heir on the safety. We prefer that they not see topics related to violence, drugs, or other adult themes. "

    answer = response_trial(level_prompt,user_prompt)
    lst = answer.split(",")
    print(lst)
    if lst[0] == "none":
        data = {"type": "none"}
    else:
        data = dict()
        for item in lst:
            components = item.split(":")
            data[components[0].strip()] = components[1].strip()
    
    return data

if __name__ == "__main__":
    while True:
        user_inp = input("Enter an object to classify: ")
        llm_classify_object(user_inp)

# Type Structure

# ALL non-null types have these parameters:
#
# "color": string (#FFFFFF), <- Optional
# "sub_color": string (#FFFFFF) <- Optional [like, if an object has 2 colors... its ok if this one doesnt work well]
# "size": string ... must be either ("wide", "tall", "small", "big")
# "dynamic": float ([0, 1]), <- Optional [ like, how expressive the word is ]

# ## Fluids
#
# response = {
#     "type": "fluid",
# }
#
# ## Inanimate Solids
#
# response = {
#     "type": "inanimate_solid",
#     "dynamic": float ([0, 1]), <- Optional
#     "physics_type": string ("mobile" | "rigid") [rigid are thiings like brick, rocks, house ... immovable objects in games; mobile are things you can push, like a bottle or something small]
# }

# ## Life
#
# response = {
#     "type": "life",
#     "movement_type": string ("land", "air", "fluid"),
#     "activity": float ([0, 1]) [how much this critter would movev around, how fast, etc.]
# }
