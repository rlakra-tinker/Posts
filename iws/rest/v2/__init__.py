#
# Author: Rohtash Lakra
#
from flask import Blueprint

from rest.account.v2 import bp as account_v2_bp
from rest.contact.v2 import bp as contact_v2_bp
from rest.role.v2 import bp as role_v2_bp

bp = Blueprint("v2", __name__, url_prefix="/v2")
"""
Create an instance of Blueprint prefixed with '/bp' as named bp.
Parameters:
    name: "v2", is the name of the blueprint, which Flask’s routing mechanism uses and identifies it in the project.
    __name__: The Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
    url_prefix: the path to prepend to all of the Blueprint’s URLs.
"""

# Register REST APIs (end-points) here
bp.register_blueprint(role_v2_bp)
bp.register_blueprint(account_v2_bp)
bp.register_blueprint(contact_v2_bp)
