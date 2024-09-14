from flask import Flask, request, json
from llm_client import binary_response_prompt

app = Flask(__name__) 

# Test routes for setup
# Pass the required route to the decorator. 
@app.route("/hello") 
def hello(): 
    return "Hello World!"
    
@app.route("/") 
def index(): 
    return "Homepage for the Flask app"

@app.route("/binary_question")
def binary_question():
    level_prompt = request.args.get('level_prompt')
    user_prompt = request.args.get('user_prompt')
    try:
        data = binary_response_prompt(level_prompt, user_prompt)

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response
    except:
        return "Error: Invalid query"
  
if __name__ == "__main__": 
    app.run(debug=True) 