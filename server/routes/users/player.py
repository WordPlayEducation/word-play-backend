from flask import Flask 
  
app = Flask(__name__) 

# Test routes for setup
# Pass the required route to the decorator. 
@app.route("/hello") 
def hello(): 
    return "Hello World!"
    
@app.route("/") 
def index(): 
    return "Homepage for the Flask app"
  
if __name__ == "__main__": 
    app.run(debug=True) 