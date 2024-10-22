#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import importlib.metadata
import os
from typing import Any
from flask import Flask, Blueprint, make_response, jsonify, current_app
from pathlib import Path
from flask_log_request_id import RequestID, RequestIDLogFilter
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.exceptions import NotFound
# https://flask.palletsprojects.com/en/3.0.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import requests
from common.config import Config
from webapp.routes import bp as webapp_bp
from api import bp as api_bp
from rest import bp as rest_bp
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity
from globals import connector


class WebApp:
    """Create WebApp class"""
    __HOST = 'host'
    __PORT = 'port'
    __DEBUG = 'debug'

    def __init__(self):
        self.path = Path()
        self.basedir = str(self.path.cwd())
        # print(f"basedir: {self.basedir}")
        self.env: dict = {}
        self.app: Flask = None

    def _load_env(self):
        with self.app.app_context():
            current_app.logger.debug(f"FLASK_ENV={os.getenv('FLASK_ENV')}")
            # Load the environment variables
            env_file_path = self.path.cwd().joinpath('.env')  # self.path.cwd() / '.env'
            current_app.logger.debug(f"env_file_path={env_file_path}")

            # loads .env file and updates the local env object
            load_dotenv(dotenv_path=env_file_path)
            self.set_env(self.__HOST, os.getenv(self.__HOST, "127.0.0.1"))
            self.set_env(self.__PORT, os.getenv(self.__PORT, '8080'))
            self.set_env(self.__DEBUG, os.getenv(self.__DEBUG, False))
            current_app.logger.debug(f"env={self.env}")

    def set_env(self, key: str, value: Any):
        self.env[key] = value

    def get_env(self, key: str) -> Any:
        return self.env.get(key, None)

    def run(self):
        """Loads Configurations and Runs Web Application"""
        host = self.get_env(self.__HOST)
        port = self.get_env(self.__PORT)
        debug = self.get_env(self.__DEBUG)
        with self.app.app_context():
            current_app.logger.debug(f"host={host}, port={port}, debug={debug}")

        # run application with params
        self.app.run(host=host, port=port, debug=debug, load_dotenv=True)

    def create_app(self, config_class: Config = Config, test_mode: bool = False) -> Flask:
        """
        Create an application your application factory pattern.

        With an application factory, your project’s structure becomes more organized.
        It encourages you to separate different parts of your application, like routes, configurations, and initializations,
        into different files later on. This encourages a cleaner and more maintainable codebase.
        """
        # create a new flask application object
        app = Flask(__name__)
        RequestID(app)
        flask_version = importlib.metadata.version("flask")
        # app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
        app.wsgi_app = ProxyFix(app.wsgi_app)
        # wsgi_app = ProxyFix(app.wsgi_app)
        self.app = app
        self._load_env()

        with self.app.app_context():
            current_app.logger.debug(
                f"Running Application [{app.name}] on version [{flask_version}] with testMode [{test_mode}] ...")

        # print(f"Running Application [{app.name}] on version [{flask.__version__}] with testMode [{test_mode}] ...")
        # print(f"Running Application [{app.name}] on version [{flask_version}] with testMode [{test_mode}] ...")

        # load app's configs
        app.config.from_object(config_class)

        # Check CORS Enabled
        if Config.CORS_ENABLED:
            CORS(app)

        # register logger here root logger
        log_file_name = 'iws.log'
        log_handler = logging.FileHandler(log_file_name)
        log_format = "%(asctime)s:%(levelname)s:%(request_id)s - %(message)s"
        print(f"log_format={log_format}")
        logging.Formatter("%(asctime)s:%(levelname)s:%(request_id)s - %(message)s")  # make the format more compact
        log_handler.addFilter(RequestIDLogFilter())  # Adds request-ID filter
        print(f"log_handler=[{log_handler}]")
        # logging.getLogger().addHandler(log_handler)
        logging.basicConfig(filename=log_file_name, level=logging.DEBUG,
                            format="%(asctime)s:%(levelname)s - %(message)s")
        requests.packages.urllib3.add_stderr_logger()

        # Initialize/Register Flask Extensions/Components, if any
        if not test_mode:
            connector.init(app)

        # Initialize/Register Default Error Handlers, if any
        @app.errorhandler(404)
        def not_found(error):
            current_app.logger.debug(f'errorClass={type(error)}, error={error}')
            if isinstance(error, NotFound):
                return make_response(jsonify('Not Found!'), 404)
            else:
                return make_response(jsonify(ErrorEntity.error(HTTPStatus.NOT_FOUND)), 404)

        @app.errorhandler(400)
        def bad_request(error):
            current_app.logger.debug(f'errorClass={type(error)}, error={error}')
            return make_response(jsonify(ErrorEntity.error(HTTPStatus.BAD_REQUEST)), 400)

        @app.errorhandler(500)
        def app_error(error):
            current_app.logger.debug(f'errorClass={type(error)}, error={error}')
            return make_response(jsonify(ErrorEntity.error(HTTPStatus.INTERNAL_SERVER_ERROR)), 500)

        # Initialize/Register Blueprints, if any

        """
        Create an instance of Blueprint prefixed with '/posts' as named bp.
        Parameters:
            name: "ws - web server", is the name of the blueprint and identifies it in the Flask project.
            __name__: The name of blueprint and used later when you import api into' app.py'.
            url_prefix: the web url prefixed with '/posts'
        """
        bp = Blueprint("iws", __name__, url_prefix="/posts")

        # register more app's here.
        bp.register_blueprint(webapp_bp)
        bp.register_blueprint(rest_bp)
        bp.register_blueprint(api_bp)

        # Register root blueprint with app that connects an app with other end-points
        app.register_blueprint(bp)

        # Initialize/Register Request's behavior/db connection
        if not test_mode:
            connector.init_db()
            connector.init_SQLAlchemy()
            # app.before_request(connector.open_connection())
            # app.teardown_request(connector.close_connection())

        return app
