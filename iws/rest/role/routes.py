#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
from rest.role.v1 import bp as bp_role_v1
from flask import make_response, request, session, redirect, url_for, abort, current_app
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity, ResponseEntity
from framework.exceptions import DuplicateRecordException
from rest.role.service import RoleService
from rest.role.models import Role
import json

# account's service
roleService = RoleService()


@bp_role_v1.post("/")
def create():
    current_app.logger.debug(f"request: {request}")
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
            response = ResponseEntity.build_response(HTTPStatus.CREATED, entity=role,
                                                     message="Role is successfully created.")
        except DuplicateRecordException as ex:
            message = f"Role={role.name} is already created! ex:{ex}"
            error = ErrorEntity.error(HTTPStatus.INTERNAL_SERVER_ERROR, message, exception=ex)
            response = ResponseEntity.build_response(HTTPStatus.INTERNAL_SERVER_ERROR, error, exception=ex)
        except Exception as ex:
            error = ErrorEntity.error(HTTPStatus.INTERNAL_SERVER_ERROR, str(ex), exception=ex)
            response = ResponseEntity.build_response(HTTPStatus.INTERNAL_SERVER_ERROR, error, exception=ex)
    else:
        response = errors

    current_app.logger.debug(f"response: {response}")
    # return make_response(response)
    return redirect(url_for("iws.webapp.contact"))


@bp_role_v1.get("/")
def get():
    params = request.args
    print(f"request:{request}, params: {params}")
    if params:
        role = roleService.find_by_id(params['id'])
        print(f"role:{role}")
        if role:
            response = ResponseEntity.response(HTTPStatus.OK, entity=role)
            return make_response(response)
        else:
            error = ErrorEntity.error(HTTPStatus.NOT_FOUND, message='No round found with ID!')
            response = ResponseEntity.response(HTTPStatus.NOT_FOUND, error)
            return abort(response)
