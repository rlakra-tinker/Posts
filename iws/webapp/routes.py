#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import Blueprint, make_response, jsonify, render_template

# bp = Blueprint("webapp", __name__, static_folder="static", static_url_path="assets", template_folder="templates")
bp = Blueprint("webapp", __name__)
"""
Create an instance of it named bp.
The first argument, "views", is the name of your blueprint and identifies this blueprint in your Flask project.
The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.


Define all web routes here like 'home/index', about and services views.
Each of them returns a string to indicate on which page you are on.

By default, Flask expects your templates to be in a "templates/" directory.
"""


# Health probe endpoint
@bp.route('/health-check/')
def health_check():
    """
    TODO: Add a check that server is up.
    :return:
    """

    return make_response(jsonify({'message': 'ok'}), 200)


# Index/Home Page
@bp.get("/")
def index():
    """
    Index Page
    """
    return render_template("index.html")


# About Page
@bp.get("/about-us")
def about():
    """
    About Us Page
    """
    return render_template("about.html")


# Services Page
@bp.get("/services")
def services():
    """
    Services Page
    """
    return render_template("services.html")


# Clients Page
@bp.get("/clients")
def clients():
    """
    Clients Page
    """
    return render_template("clients.html")


# Contact Us Page
# @bp.route("/contact-us", methods=[HTTPMethod.GET.name, HTTPMethod.POST.name])
@bp.get("/contact-us")
def contact():
    """
    Contact Us Page
    """
    # if HTTPMethod.is_post(request.method):
    #     print(request.get_json())
    #     response = create()

    return render_template("contact.html")


# Logout Page
@bp.get("/logout")
def logout():
    """
    About Us Page
    """
    return render_template("logout.html")
