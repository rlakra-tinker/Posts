#
# Author: Rohtash Lakra
#
from flask import request, g, render_template, make_response, jsonify
from framework.utils import HTTPMethod, HTTPStatus
from . import bp as v1_account


@v1_account.route('/', methods=[HTTPMethod.POST])
def create_account():
    # Creates a new account
    pass
