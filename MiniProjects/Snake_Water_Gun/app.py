# Here's a Simple Flask App Skeleton Code that we use for the Snake-Water-Gun Game
'''
from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

'''
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Possible choices
choices = ["snake", "water", "gun"]

# Mapping of winning relationships
dwins = {
    ("snake", "water"),  # snake drinks water
    ("water", "gun"),    # water douses gun
    ("gun", "snake"),    # gun kills snake
}

@app.route("/", methods = ["GET", "POST"])
def index():
    result = None
    user_choice = None
    comp_choice = None

    if request.method == "POST":
        user_choice = request.form.get("choice", None)
        comp_choice = random.choice(choices)
        if user_choice == comp_choice:
            result = "Draw"
        elif (user_choice, comp_choice) in dwins:
            result = "You Win!"
        else:
            result = "You Lose!"

    return render_template("index.html", user_choice=user_choice, comp_choice=comp_choice, result=result)

if __name__ == "__main__":
    app.run(debug=True)
