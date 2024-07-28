#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
from flask import Flask, Blueprint
from pathlib import Path

from .routes import bp as webapp_bp
from api import bp as api_bp
from rest import bp as rest_bp

"""
Create WebApp class
"""


def create_app(testMode=False):
    """
    Create an application your application factory pattern.

    With an application factory, your project’s structure becomes more organized.
    It encourages you to separate different parts of your application, like routes, configurations, and initializations,
    into different files later on. This encourages a cleaner and more maintainable codebase.
    """
    # create flask application
    app = Flask(__name__)

    if testMode:
        print("Running Test Application ...")

    # register logger here root logger

    """
    Create an instance of it named bp.
    The first argument, "webapp", is the name of your blueprint and identifies this blueprint in your Flask project.
    The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
    """
    bp = Blueprint("iws", __name__, url_prefix="/posts-iws")

    # register more app's here.
    bp.register_blueprint(webapp_bp)
    bp.register_blueprint(api_bp)
    bp.register_blueprint(rest_bp)

    # Connect the 'ews-posts' blueprint with your Flask project
    app.register_blueprint(bp)

    return app


class WebApp:

    def __init__(self):
        self.path = Path()
        self.basedir = str(self.path.cwd())
        print(f"basedir: {self.basedir}")
        self.load_env()

    def load_env(self):
        # Load the environment variables
        envars = self.path.cwd() / '.env'
        print(f"envars:{envars}")
        print()
        # load_dotenv(envars)

