#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import Blueprint, make_response, jsonify, render_template

bp = Blueprint("webapp", __name__)
# bp = Blueprint("webapp", __name__, static_folder="static", static_url_path="assets", template_folder="templates")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: "webapp", is the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.

Define all web routes here like 'home/index', about and services views.
Each of them returns a string to indicate on which page you are on.

By default, Flask expects your templates to be in a "templates/" directory.
"""


@bp.route('/health-check/')
def health_check():
    """Application's Health-check Endpoint
    TODO: Add a check that server is up.
    :return:
    """

    return make_response(jsonify({'message': 'ok'}), 200)


@bp.get("/")
def index():
    """Index/Home Page"""
    return render_template("index.html")


@bp.get("/about-us")
def about():
    """About Us Page"""
    return render_template("about.html")


@bp.get("/services")
def services():
    """Services Page"""
    return render_template("services.html")


@bp.get("/clients")
def clients():
    """Clients Page"""
    return render_template("clients.html")


# @bp.route("/contact-us", methods=[HTTPMethod.GET.name, HTTPMethod.POST.name])
@bp.get("/contact-us")
def contact():
    """Contact Us Page"""
    # if HTTPMethod.is_post(request.method):
    #     print(request.get_json())
    #     response = create()

    return render_template("contact.html")


@bp.get("/logout")
def logout():
    """Logout Page"""
    return render_template("logout.html")