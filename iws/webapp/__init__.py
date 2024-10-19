#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-project/
#
from .app import WebApp

webApp = WebApp()
app = webApp.create_app()

# App Main
if __name__ == "__main__":
    """
    Main Application

    How to run:
    - python3 webapp.py
    - python -m flask --app webapp run --port 8080 --debug
    """
    # create an app
    webApp.run(app)