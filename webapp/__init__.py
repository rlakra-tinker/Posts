#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
from flask import Flask, Blueprint
from webapp.templates import views
from webapp import api

"""
Create an application your application factory pattern.

With an application factory, your project’s structure becomes more organized.
It encourages you to separate different parts of your application, like routes, configurations, and initializations,
into different files later on. This encourages a cleaner and more maintainable codebase.
"""


def create_app():
    # create flask application
    app = Flask(__name__)

    # register logger here root logger

    """
    Create an instance of it named bp.
    The first argument, "webapp", is the name of your blueprint and identifies this blueprint in your Flask project.
    The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
    """
    bp = Blueprint("webapp", __name__, url_prefix="/posts-ews")

    # register more app's here.
    bp.register_blueprint(views.bp)
    bp.register_blueprint(api.bp)

    # Connect the 'ews-posts' blueprint with your Flask project
    app.register_blueprint(bp)

    return app
