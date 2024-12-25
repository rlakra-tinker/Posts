#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging

from flask import make_response, request, abort

from framework.exception import DuplicateRecordException, ValidationException
from framework.http import HTTPStatus
from framework.model import ErrorModel, ResponseModel
from framework.utils import Utils
from rest.role.model import Role
from rest.role.service import RoleService
from rest.role.v1 import bp as bp_role_v1

logger = logging.getLogger(__name__)


# class RoleController:
#
#     # roleService = RoleService()
#
#     def __init__(self):
#         logger.debug("RoleController()")
#         self.roleService = RoleService()

@bp_role_v1.post("/")
def create():
    logger.debug(f"create => {request}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        role = Role(**body)
        logger.debug(f"role={role}")
        # role = RoleSchema(name=name, active=active)
        # role = Role.create(name=name, active=active)

    try:
        roleService = RoleService()
        roleService.validate(role)
        role = roleService.create(role)
        logger.debug(f"role={role}")

        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="Role is successfully created.")
        response.addInstance(role)
        # response = response.to_json()
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.post("/batch")
def create_batch():
    logger.debug(f"create => {request}")
    try:
        roles = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
            if isinstance(body, list):
                roles = [Role(**entry) for entry in body]
            elif isinstance(body, dict):
                roles.append(Role(**body))
            else:
                # handle form fields here.
                pass

        logger.debug(f"roles={roles}")
        roleService = RoleService()
        roleService.validates(roles)
        roles = roleService.createBatch(roles)
        logger.debug(f"roles={roles}")

        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="Roles are successfully created.")
        response.addInstances(roles)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.get("/")
def get():
    logger.debug(f"get => {request}, request.args={request.args}, is_json:{request.is_json}")
    params = request.args
    try:
        roleService = RoleService()
        roles = roleService.findAll(params)
        logger.debug(f"roles={roles}")

        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if not roles:
            response.message = "No Records Exists!"
        response.addInstances(roles)
        logger.debug(f"response={response}")
        return make_response(response.to_json(), response.status)
    except Exception as ex:
        logger.error(f"Error={ex}, stack_trace={Utils.stack_trace(ex)}")
        error = ErrorModel.buildError(HTTPStatus.NOT_FOUND, message='No round found with ID!', exception=ex)
        response = ResponseModel.buildResponse(HTTPStatus.NOT_FOUND, error)
        return abort(response.to_json(), response.status)
