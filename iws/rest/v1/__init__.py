#
# Author: Rohtash Lakra
#
from flask import Blueprint
from iws.rest.role.routes import bp as role_bp
from iws.rest.account.routes import bp as accounts_bp
from iws.rest.contact.routes import bp as contact_bp

#
bp = Blueprint("v1", __name__, url_prefix="/v1")
"""
Create an instance of it named 'bp'. 
The first argument, "api_v1", is the name of your blueprint and identifies this blueprint in your Flask project.
The second argument is the blueprint’s '__name__' and used later when you import api into' webapp.py'.
"""


# register end-points here
bp.register_blueprint(role_bp)
bp.register_blueprint(accounts_bp)
bp.register_blueprint(contact_bp)
