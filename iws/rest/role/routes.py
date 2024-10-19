#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
from flask import Blueprint, make_response, request, session, redirect, url_for, abort, current_app
from iws.framework.http import HTTPStatus
from iws.framework.model.abstract import ErrorEntity, ResponseEntity
from iws.framework.exceptions import DuplicateRecordException
from iws.rest.role.service import RoleService
from iws.rest.role.models import Role
import json

#
bp = Blueprint("roles", __name__, url_prefix="/roles")
"""
Making a Flask Blueprint:

Create an instance of it named 'bp'.

Note that in the below code, some arguments are specified when creating the Blueprint object.
The first argument, 'api', is the Blueprint’s name, which is used by Flask’s routing mechanism (and identifies it in your Flask project). 
The second argument, '__name__', is the Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
The third argument, 'url_prefix="/api"', the path to prepend to all of the Blueprint’s URLs.

There are other optional arguments that you can provide to alter the Blueprint’s behavior:

static_folder: the folder where the Blueprint’s static files can be found
static_url_path: the URL to serve static files from
template_folder: the folder containing the Blueprint’s templates
url_prefix: the path to prepend to all of the Blueprint’s URLs
subdomain: the subdomain that this Blueprint’s routes will match on by default
url_defaults: a dictionary of default values that this Blueprint’s views will receive
root_path: the Blueprint’s root directory path, whose default value is obtained from the Blueprint’s import name

Note that all paths, except root_path, are relative to the Blueprint’s directory.

However, a Flask Blueprint is not actually an application. It needs to be registered in an application before you can run it. 
When you register a Flask Blueprint in an application, you’re actually extending the application with the contents of the Blueprint.
This is the key concept behind any Flask Blueprint. They record operations to be executed later when you register them on an application.

The Blueprint object 'bp' has methods and decorators that allow you to record operations to be executed when registering 
the Flask Blueprint in an application to extend it.

Here are the Blueprint objects most used decorators that you may find useful:

- '.route()' to associate a view function to a URL route
- '.errorhandler()' to register an error handler function
- '.before_request()' to execute an action before every request
- '.after_request()' to execute an action after every request
- '.app_template_filter()' to register a template filter at the application level

When you register the Flask Blueprint in an application, you extend the application with its contents.

"""

# account's service
roleService = RoleService()


@bp.post("/")
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


@bp.get("/")
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

