#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
import logging
from datetime import datetime

from flask import make_response, request
from flask import session, g, redirect, url_for

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.model import ErrorModel
from framework.model import ResponseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from rest.user.model import User
from rest.user.service import UserService
from rest.user.v1 import bp as bp_account_v1

logger = logging.getLogger(__name__)

userService = UserService()


@bp_account_v1.before_app_request
def loadLoggedInUser():
    """Load LoggedIn User"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # g.user = userService.find_by_id(user_id)
        g.user = None


@bp_account_v1.post("/register")
def register():
    """Register User"""
    logger.debug(
        f"+register() => request={request}, args={request.args}, is_json:{request.is_json}, form:{request.form}")
    try:
        body = None
        if request.is_json:
            body = request.get_json()
            # user = UserSchema(**request.get_json())
            # user = userService.register()
            # user = UserSchema.model_construct(request.get_json())
            # user = userService.create(user)
            # return user, 201

        elif request.form:
            logger.debug(f"request.form={request.form}")
            body = request.form.to_dict()

        if not body:
            raise ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=["'User' is not fully defined!"])

        # body["birth_date"] = datetime.now().strftime("%Y-%m-%d")
        logger.debug(f"body={body}")
        # user = User.model_validate(obj=body)
        user = User(**body)
        logger.debug(f"user={user}")
        # userService = UserService()
        userService.validate(SchemaOperation.CREATE, user)
        user = userService.create(user)
        # user = userService.register(username, password)

        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="User is successfully created.")
        response.addInstance(user)
        # response = response.to_json()
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
        return redirect(url_for("iws.api.login"), response)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    # flash(error)
    logger.debug(f"-register() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_account_v1.post("/login")
def login():
    """Login User"""
    logger.debug(f"+login() => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        user = request.get_json()
        print(f"user:{user}")
        # if not accounts:
        #     for user in accounts:
        #         if user['user_name'] == user.user_name:
        #             return make_response(HTTPStatus.OK, user)

    response = ErrorModel.buildError(HTTPStatus.NOT_FOUND, "Account is not registered!")
    print(response)

    return make_response(response)


# Logout Page
@bp_account_v1.post("/logout")
def logout():
    """Logout User"""
    logger.debug(f"+logout() => request={request}, args={request.args}, is_json:{request.is_json}")
    session.clear()


@bp_account_v1.post("/forgot-password")
def forgot_password():
    """Forgot User's Password"""
    logger.debug(f"+forgot_password() => request={request}, args={request.args}, is_json:{request.is_json}")
    pass


@bp_account_v1.post("/")
def create():
    """Create/Register User"""
    logger.debug(f"+create() => request={request}, args={request.args}, is_json:{request.is_json}")
    # post_data = request.form.to_dict(flat=False)
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        user = User(**body)
        logger.debug(f"user={user}")
        # user = RoleSchema(name=name, active=active)
        # user = User.create(name=name, active=active)

    try:
        userService = UserService()
        userService.validate(SchemaOperation.CREATE, user)
        user = userService.create(user)
        logger.debug(f"user={user}")
        # build success response
        response = ResponseModel(status=HTTPStatus.CREATED.status_code, message="User is successfully created.")
        response.addInstance(user)
        # response = response.to_json()
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except DuplicateRecordException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-create() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_account_v1.post("/batch")
def bulkCreate():
    """Create/Register Bulk Users"""
    logger.debug(f"+bulkCreate() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        roles = []
        if request.is_json:
            body = request.get_json()
            logger.debug(f"type={type(body)}, body={body}")
            if isinstance(body, list):
                roles = [User(**entry) for entry in body]
            elif isinstance(body, dict):
                roles.append(User(**body))
            else:
                # handle form fields here.
                pass

        logger.debug(f"roles={roles}")
        userService = UserService()
        userService.validates(SchemaOperation.CREATE, roles)
        roles = userService.bulkCreate(roles)
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


@bp_account_v1.get("/")
def get():
    """Get User"""
    logger.debug(f"+get() => request={request}, args={request.args}, is_json:{request.is_json}")
    try:
        userService = UserService()
        roles = userService.findByFilter(request.args)

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


@bp_account_v1.put("/")
def update():
    """Update User"""
    logger.debug(f"+update() => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        user = User(**body)
        logger.debug(f"user={user}")

    try:
        userService = UserService()
        userService.validate(SchemaOperation.UPDATE, user)
        user = userService.update(user)
        logger.debug(f"user={user}")

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.status_code, message="User is successfully updated.")
        response.addInstance(user)
    except ValidationException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-update() <= response={response}")
    return make_response(response.to_json(), response.status)


@bp_account_v1.delete("/<id>")
def delete(id: int):
    """Delete a User"""
    logger.debug(f"+delete({id}) => request={request}, args={request.args}, is_json:{request.is_json}")
    if request.is_json:
        body = request.get_json()
        logger.debug(f"body={body}")
        user = User(**body)
        logger.debug(f"user={user}")

    try:
        userService = UserService()
        userService.delete(id)

        # build success response
        response = ResponseModel(status=HTTPStatus.OK.status_code, message="User is successfully deleted.")
    except NoRecordFoundException as ex:
        response = ResponseModel.buildResponseWithException(ex)
    except Exception as ex:
        response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(ex), exception=ex)

    logger.debug(f"-delete() <= response={response}")
    return make_response(response.to_json(), response.status)