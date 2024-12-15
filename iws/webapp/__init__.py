#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import importlib.metadata
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from framework.logger import DefaultLogger

import requests
from dotenv import load_dotenv
from flask import Flask, Blueprint, make_response, jsonify, current_app, request
from flask_cors import CORS
from flask_log_request_id import RequestIDLogFilter
from werkzeug.exceptions import NotFound
# https://flask.palletsprojects.com/en/3.0.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix

from api import bp as api_bp
from common.config import Config
from framework.enums import EnvType
from framework.enums import KeyEnum
from framework.http import HTTPStatus
from framework.model.abstract import ErrorModel
from globals import connector
from rest import bp as rest_bp
from webapp.routes import bp as webapp_bp


class WebApp:
    """Create WebApp class"""
    __HOST = 'host'
    __PORT = 'port'
    __DEBUG = 'debug'
    __FLASK_ENV = 'FLASK_ENV'
    __ENV_TYPE = 'env_type'
    __LOG_FILE_NAME = 'LOG_FILE_NAME'

    def __init__(self):
        self.path = Path()
        self.basedir = str(self.path.cwd())
        print(f"basedir={self.basedir}")
        # sys.path.append(self.basedir)
        print(f"sys.path={sys.path}")
        self.environment: dict = {}
        self.app: Flask = None

    def _load_env(self, test_mode: bool = False):
        with self.app.app_context():
            flask_version = importlib.metadata.version("flask")
            current_app.logger.debug(
                f"Running Application [{self.app.name}] on version [{flask_version}] with testMode [{test_mode}] ...")
            current_app.logger.debug(f"FLASK_ENV={os.getenv(self.__FLASK_ENV)}")
            # Load the environment variables
            env_file_path = self.path.cwd().joinpath('.env')  # self.path.cwd() / '.env'
            current_app.logger.debug(f"env_file_path={env_file_path}")

            # loads .env file and updates the local env object
            load_dotenv(dotenv_path=env_file_path)
            self.set_env(self.__HOST, os.getenv(self.__HOST, "127.0.0.1"))
            self.set_env(self.__PORT, os.getenv(self.__PORT, '8080'))
            self.set_env(self.__DEBUG, os.getenv(self.__DEBUG, False))
            self.set_env(self.__ENV_TYPE, os.getenv(self.__FLASK_ENV, 'Development'))
            self.set_env(self.__LOG_FILE_NAME, os.getenv(self.__LOG_FILE_NAME, 'iws.log'))
            current_app.logger.debug(f"environment={self.environment}")

    def set_env(self, key: str, value: Any):
        self.environment[key] = value

    def get_env(self, key: str) -> Any:
        return self.environment.get(key, None)

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
        # app = connexion.App(__name__, specification_dir="./")
        # app.add_api("swagger.yml")

        # use custom logger adapter
        app.logger = DefaultLogger(app, {})

        # app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
        app.wsgi_app = ProxyFix(app.wsgi_app)
        # wsgi_app = ProxyFix(app.wsgi_app)
        self.app = app
        self._load_env(test_mode=test_mode)
        # load app's configs
        app.config.from_object(config_class)

        # Check CORS Enabled
        if Config.CORS_ENABLED:
            CORS(app)

        # register logger here root logger
        if EnvType.is_production(self.get_env(self.__ENV_TYPE)):
            log_file_name = self.get_env(self.__LOG_FILE_NAME)
            log_handler = logging.FileHandler(log_file_name)
            log_format = "%(asctime)s:%(levelname)s:%(request_id)s - %(message)s"
            logging.Formatter("%(asctime)s:%(levelname)s:%(request_id)s - %(message)s")  # make the format more compact
            log_handler.addFilter(RequestIDLogFilter())  # Adds request-ID filter
            with self.app.app_context():
                current_app.logger.debug(f"log_format={log_format}")
                current_app.logger.debug(f"log_handler=[{log_handler}]")
            # logging.getLogger().addHandler(log_handler)
            logging.basicConfig(filename=log_file_name, encoding='utf-8', level=logging.DEBUG,
                                format="%(asctime)s:%(levelname)s - %(message)s")
            requests.packages.urllib3.add_stderr_logger()

        # Initialize/Register Flask Extensions/Components, if any
        if not test_mode:
            connector.init(app)

        # Initialize/Register Default Error Handlers, if any

        @app.errorhandler(404)
        def not_found(error):
            """404 - NotFound Error Handler"""
            current_app.logger.error(f'request={request}, errorClass={type(error)}, error={error}')
            if isinstance(error, NotFound):
                current_app.logger.error(f'NotFound => request={request}, errorClass={type(error)}, error={error}')
                return make_response(jsonify('Not Found!'), 404)
            else:
                # return make_response(jsonify(ErrorEntity.error(HTTPStatus.NOT_FOUND).to_json()), 404)
                # return make_response(ErrorEntity.error(HTTPStatus.NOT_FOUND).to_json(), 404)
                return make_response(json.dumps(ErrorModel.error(HTTPStatus.NOT_FOUND)), 404)

        @app.errorhandler(400)
        def bad_request(error):
            """400 - BadRequest Error Handler"""
            current_app.logger.error(f'request={request}, errorClass={type(error)}, error={error}')
            # return make_response(jsonify(ErrorEntity.error(HTTPStatus.BAD_REQUEST).to_json()), 400)
            return make_response(ErrorModel.error(HTTPStatus.BAD_REQUEST).to_json(), 400)

        @app.errorhandler(500)
        def app_error(error):
            """500 - InternalServer Error Handler"""
            current_app.logger.error(f'request={request}, errorClass={type(error)}, error={error}')
            return make_response(jsonify(ErrorModel.error(HTTPStatus.INTERNAL_SERVER_ERROR)), 500)
            return make_response(ErrorModel.error(HTTPStatus.INTERNAL_SERVER_ERROR).to_json(), 500)

        # Register Date & Time Formatter for Jinja Template
        @app.template_filter('strftime')
        def _jinja2_filter_datetime(date_str, datetime_format: str = None):
            """Formats the date_str"""
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            native = date.replace(tzinfo=None)
            if datetime_format:
                return native.strftime(datetime_format)
            else:
                return native.strftime("%b %d, %Y at %I:%M%p")

        # Initialize/Register Blueprints, if any

        """
        Create an instance of Blueprint prefixed with '/bp' as named bp.
        Parameters:
            name: "iws", is the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
            __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
            url_prefix: the path to prepend to all of the Blueprint’s URLs.
        """
        # bp = Blueprint("iws", __name__, url_prefix="/posts")
        bp = Blueprint("iws", __name__)

        # register more app's here.
        bp.register_blueprint(rest_bp)
        bp.register_blueprint(api_bp)
        bp.register_blueprint(webapp_bp)

        # Register root blueprint with app that connects an app with other end-points
        app.register_blueprint(bp)

        # Initialize/Register Request's behavior/db connection
        if not test_mode:
            connector.init_db({KeyEnum.DB_TYPE: KeyEnum.SQLALCHEMY})
            # app.before_request(connector.open_connection())
            # app.teardown_request(connector.close_connection())

        return app
