#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging

from flask import make_response, request

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
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
    logger.debug(f"+create() => request={request}, args={request.args}, is_json:{request.is_json}")
    # post_data = request.form.to_dict(flat=False)
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        role = Role(**body)
        logger.debug(f"role={role}")
        # role = RoleSchema(name=name, active=active)
        # role = Role.create(name=name, active=active)

    try:

        roleService = RoleService()
        roleService.validate(SchemaOperation.CREATE, role)
        role = roleService.create(role)
        logger.debug(f"role={role}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="Role is successfully created.")
        response.addInstance(role)
        # response = response.to_json()
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-create() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.post("/batch")
def bulkCreate():
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
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
                body = request.form.to_dict()
                roles.append(Role(**body))

        logger.debug(f"roles={roles}")
        roleService = RoleService()
        roleService.validates(SchemaOperation.CREATE, roles)
        roles = roleService.bulkCreate(roles)
        logger.debug(f"roles={roles}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="Roles are successfully created.")
        response.addInstances(roles)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-bulkCreate() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.get("/")
def get():
    logger.debug(f"+get() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        roleService = RoleService()
        roles = roleService.findByFilter(request.args)

        # build success response
        response = ResponseModel.buildResponse(HTTPStatus.OK)
        if roles:
            response.addInstances(roles)
        else:
            response.message = "No Records Exist!"
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-get() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.put("/")
def update():
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        if request.is_json:
            body = request.get_json()
            logger.debug(f"body={body}")
            role = Role(**body)
            logger.debug(f"role={role}")

        roleService = RoleService()
        roleService.validate(SchemaOperation.UPDATE, role)
        role = roleService.update(role)
        logger.debug(f"role={role}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.status_code, message="Role is successfully updated.")
        response.addInstance(role)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except NoRecordFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_role_v1.delete("/<id>")
def delete(id: int):
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        role = Role(**body)
        logger.debug(f"role={role}")

    try:
        roleService = RoleService()
        roleService.delete(id)

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.status_code, message="Role is successfully deleted.")
    except NoRecordFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)
