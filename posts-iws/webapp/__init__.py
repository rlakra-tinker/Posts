#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
import os
from .app import create_app

# init app by calling crate api function.
app = create_app()


def run_app():
    """
    Run Web Application

    Configure the app here.
    """
    # localhost
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8080))
    debug = bool(os.getenv("DEBUG_ENABLED", True))

    # run application with params
    app.run(host=host, port=port, debug=debug)


"""
Main Application

How to run:
- python3 webapp.py
- python -m flask --app webapp run --port 8080 --debug

"""
# App Main
if __name__ == "__main__":
    run_app()
