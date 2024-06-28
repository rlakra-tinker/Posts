#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import os
from flask import Flask
import api

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

    # Connect the 'api' blueprint with your Flask project
    app.register_blueprint(api.bp)

    return app


# init app by calling crate api function.
app = create_app()


"""
Run Web Application

Configure the app here.
"""

def run_web_app():
    # localhost
    host = os.getenv("APP_HOST_NAME", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8080))
    debug = bool(os.getenv("DEBUG_ENABLED", True))

    # run application with params
    app.run(host=host, port=port, debug=debug)


"""
Main Application

How to run:
- python3 webapp.py
- python -m flask --app board run --port 8000 --debug

"""
# App Main
if __name__ == "__main__":
    run_web_app()
