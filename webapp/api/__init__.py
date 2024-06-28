from flask import Flask
from api import views

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
    app.register_blueprint(views.bp)

    return app