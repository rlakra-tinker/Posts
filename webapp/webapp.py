#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
from flask import Flask

app = Flask(__name__)

# Index Page
@app.route('/')
def index():
    return "Welcome Flask!"

# About Us
@app.route('/about')
def about():
    return "about.html"


"""
Main Application

How to run:
- python3 webapp.py
- python -m flask --app board run --port 8000 --debug

"""
# App Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
