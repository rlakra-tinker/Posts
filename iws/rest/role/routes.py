#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import json

from flask import make_response, request, abort, current_app, jsonify

from framework.exceptions import DuplicateRecordException
from framework.http import HTTPStatus
from framework.model import ErrorModel, ResponseModel
from framework.utils import Utils
from rest.role.schema import Role
from rest.role.model import Role
from rest.role.service import RoleService
from rest.role.v1 import bp as bp_role_v1

# account's service
roleService = RoleService()


@bp_role_v1.post("/")
def create():
    current_app.logger.debug(f"create => {request}")
    if request.is_json:
        body = request.get_json()
        current_app.logger.debug(f"body: {body}")
        name = body.get('name', None)
        active = body.get('active', False)
        role = Role.create(name=name, active=active)

    errors = roleService.validate(role)
    current_app.logger.debug(f"errors: {json.dumps(errors)}")
    if not errors:
        try:
            role = roleService.create(role)
            current_app.logger.debug(f"role: {role}")
            response = ResponseModel.jsonResponse(HTTPStatus.CREATED, entity=role,
                                                  message="Role is successfully created.")
        except DuplicateRecordException as ex:
            message = f"Role={role.name} is already created! ex:{ex}"
            error = ErrorModel.buildError(HTTPStatus.INTERNAL_SERVER_ERROR, message, exception=ex)
            response = ResponseModel.jsonResponse(HTTPStatus.INTERNAL_SERVER_ERROR, error, exception=ex)
        except Exception as ex:
            error = ErrorModel.buildError(HTTPStatus.INTERNAL_SERVER_ERROR, str(ex), exception=ex)
            response = ResponseModel.jsonResponse(HTTPStatus.INTERNAL_SERVER_ERROR, error, exception=ex)
    else:
        response = errors

    current_app.logger.debug(f"response: {response}")
    return make_response(jsonify(response))
    # return make_response(response)
    # TODO: REDIRECT TO LOGIN PAGE
    # return redirect(url_for("iws.webapp.contact"))


@bp_role_v1.get("/")
def get():
    current_app.logger.debug(f"get => {request}, request.args={request.args}, is_json:{request.is_json}")
    params = request.args
    # body = request.get_json() if request.is_json else {}
    # current_app.logger.debug(f"body={body}")
    try:
        roles = roleService.find_all(params)
        current_app.logger.debug(f"roles={roles}")
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        response.addData(roles)
        current_app.logger.debug(f"response={response}")
        return make_response(response.to_json())
    except Exception as ex:
        current_app.logger.error(f"Error={ex}, stack_trace={Utils.stack_trace(ex)}")
        error = ErrorModel.buildError(HTTPStatus.NOT_FOUND, message='No round found with ID!', exception=ex)
        response = ResponseModel.buildResponse(HTTPStatus.NOT_FOUND, error)
        return abort(response.to_json())
