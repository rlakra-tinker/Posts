from flask import Blueprint, render_template

"""
Create an instance of it named bp. 
The first argument, "views", is the name of your blueprint and identifies this blueprint in your Flask project.
The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
"""
bp = Blueprint("views", __name__)

"""
Then, you define two routes, one as the home view and the other as the about view. 
Each of them returns a string to indicate on which page you are on.

By default, Flask expects your templates to be in a "templates/" directory. 
"""

"""
Index Page
"""
@bp.route("/")
def index():
    return render_template("views/index.html")

"""
About Us Page
"""
@bp.route("/about")
def about():
    return render_template("views/about.html")

