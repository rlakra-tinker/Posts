#
# Author: Rohtash Lakra
#
from flask import Blueprint
from rest.account.routes import bp as accounts_bp


"""
Create an instance of it named 'bp'. 
The first argument, "api_v1", is the name of your blueprint and identifies this blueprint in your Flask project.
The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
"""
bp = Blueprint("v1", __name__, url_prefix="/v1")

# register end-points here
bp.register_blueprint(accounts_bp)
