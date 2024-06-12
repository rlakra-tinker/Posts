from flask import Flask

app = Flask(__name__)

# Index Page
@app.route('/')
def index():
    return "index.html"

# About Us
@app.route('/about')
def about():
    return "about.html"



