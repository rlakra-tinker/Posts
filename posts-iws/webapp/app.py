#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import os
from typing import Any
import flask
from flask import Flask, Blueprint, make_response, jsonify, g
from pathlib import Path
from webapp.config import Config
from webapp.routes import bp as webapp_bp
from api import bp as api_bp
from rest import bp as rest_bp
from flask_log_request_id import RequestID, RequestIDLogFilter
import logging
from flask_cors import CORS
from framework.model.abstract import ErrorEntity
from framework.http import HTTPStatus
from webapp.globals import connector
from dotenv import load_dotenv


class WebApp:
    """Create WebApp class"""
    __HOST = 'host'
    __PORT = 'port'
    __DEBUG = 'debug'

    def __init__(self):
        self.path = Path()
        self.basedir = str(self.path.cwd())
        print(f"basedir: {self.basedir}")
        self.env: dict = {}
        # self.load_env()

    def load_env(self):
        # Load the environment variables
        env_file_path = '/'.join([self.path.cwd(), '.env'])  # self.path.cwd() / '.env'
        print(f"env_file_path: {env_file_path}")
        print()

        load_dotenv(env_file_path)
        print(f"__HOST={self.__HOST}, __PORT={self.__PORT}, __DEBUG={self.__DEBUG}")
        self.set_env(self.__HOST, os.getenv("APP_HOST", "0.0.0.0"))
        self.set_env(self.__PORT, os.getenv("APP_PORT", 8080))
        self.set_env(self.__DEBUG, os.getenv("DEBUG_ENABLED", False))

        # host = os.getenv("APP_HOST", "0.0.0.0")
        # port = int(os.getenv("APP_PORT", 8080))
        # debug = bool(os.getenv("DEBUG_ENABLED", True))

    def set_env(self, key: str, value: Any):
        self.env[key] = value

    def get_env(self, key: str) -> Any:
        return self.env.get(key, None)

    def run_app(self, app: Flask = None):
        """
        Run Web Application

        Configure the app here.
        """
        self.load_env()
        host = self.get_env(self.__HOST)
        port = self.get_env(self.__PORT)
        debug = self.get_env(self.__DEBUG)
        print(f"host={host}, port={port}, debug={debug}")

        # run application with params
        app.run(host=host, port=port, debug=debug)

    def create_app(self, config_class: Config = Config, test_mode: bool = False):
        """
        Create an application your application factory pattern.

        With an application factory, your project’s structure becomes more organized.
        It encourages you to separate different parts of your application, like routes, configurations, and initializations,
        into different files later on. This encourages a cleaner and more maintainable codebase.
        """
        # create flask application
        app = Flask(__name__)
        RequestID(app)
        print(f"Running Application [{app.name}] on version [{flask.__version__}] with testMode [{test_mode}] ...")

        # load app's configs
        app.config.from_object(config_class)

        # Check CORS Enabled
        if Config.CORS_ENABLED:
            CORS(app)

        # register logger here root logger
        log_file_name = 'posts-iws-service.log'
        log_handler = logging.FileHandler(log_file_name)
        logging.Formatter("%(asctime)s:%(levelname)s:%(request_id)s - %(message)s")  # make the format more compact
        log_handler.addFilter(RequestIDLogFilter())  # Adds request-ID filter
        # logging.getLogger().addHandler(log_handler)
        print(f"log_handler=[{log_handler}]")

        # Initialize/Register Flask Extensions/Components, if any
        if not test_mode:
            connector.init(app)

        # Initialize/Register Default Error Handlers, if any
        @app.errorhandler(404)
        def not_found(error):
            return make_response(jsonify(ErrorEntity.error(HTTPStatus.NOT_FOUND)), 404)

        @app.errorhandler(400)
        def bad_request(error):
            return make_response(jsonify(ErrorEntity.error(HTTPStatus.BAD_REQUEST)), 400)

        @app.errorhandler(500)
        def app_error(error):
            return make_response(jsonify(ErrorEntity.error(HTTPStatus.INTERNAL_SERVER_ERROR)), 500)

        # Initialize/Register Blueprints, if any

        """
        Create an instance of it named bp.
        The first argument, "webapp", is the name of your blueprint and identifies this blueprint in your Flask project.
        The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
        """
        bp = Blueprint("iws", __name__, url_prefix="/posts-iws")

        # register more app's here.
        bp.register_blueprint(webapp_bp)
        bp.register_blueprint(rest_bp)
        bp.register_blueprint(api_bp)

        # Connect the 'ews-posts' blueprint with your Flask project
        app.register_blueprint(bp)

        # Initialize/Register Request's behavior/db connection
        if not test_mode:
            connector.init_db()
            connector.init_SQLAlchemy()
            # app.before_request(connector.open_connection())
            # app.teardown_request(connector.close_connection())

        return app
