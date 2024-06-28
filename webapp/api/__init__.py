#
# Author: Rohtash Lakra
#
from flask import Blueprint
from .v1 import bp as bp_v1

"""
Create an instance of it named bp. 
The first argument, "api", is the name of your blueprint and identifies this blueprint in your Flask project.
The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
"""
bp = Blueprint("api", __name__, url_prefix="/api")

# register version paths here
bp.register_blueprint(bp_v1)
