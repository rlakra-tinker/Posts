#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import BaseModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.security.hash import HashUtils
from framework.service import AbstractService
from rest.role.service import RoleService
from rest.user.mapper import UserMapper
from rest.user.model import User
from rest.user.repository import UserRepository
from rest.user.schema import UserSecuritySchema

logger = logging.getLogger(__name__)


class UserService(AbstractService):

    def __init__(self):
        logger.debug(f"UserService()")
        self.userRepository = UserRepository()

    def validate(self, operation: SchemaOperation, user: User) -> None:
        logger.debug(f"+validate({operation}, {user})")
        # super().validate(operation, user)
        error_messages = []

        # validate the object
        if user:
            match operation.name:
                case SchemaOperation.CREATE.name:
                    # validate the required fields
                    if not user.email:
                        error_messages.append("User 'email' is required!")

                    if not user.first_name:
                        error_messages.append("User 'first_name' is required!")

                    if not user.last_name:
                        error_messages.append("User 'last_name' is required!")

                    if not user.birth_date:
                        error_messages.append("User 'birth_date' is required!")

                    if not user.user_name:
                        error_messages.append("User 'user_name' is required!")

                    if not user.password:
                        error_messages.append("User 'password' is required!")

                case SchemaOperation.UPDATE.name:
                    if not user.id:
                        error_messages.append("User 'id' is required!")
        else:
            error_messages.append("'User' is not fully defined!")

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"-validate(), {type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseModel]]:
        logger.debug(f"+findByFilter({filters})")
        userSchemas = self.userRepository.findByFilter(filters)
        # logger.debug(f"userSchemas => type={type(userSchemas)}, values={userSchemas}")
        roleModels = []
        for userSchema in userSchemas:
            # logger.debug(f"userSchema type={type(userSchema)}, value={userSchema}")
            userModel = UserMapper.fromSchema(userSchema)
            # logger.debug(f"type={type(userModel)}, userModel={userModel}")
            roleModels.append(userModel)

        logger.debug(f"-findByFilter(), roleModels={roleModels}")
        return roleModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        userSchemas = self.userRepository.findByFilter(filters)
        result = True if userSchemas else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, users: List[User]) -> None:
        logger.debug(f"+validates({operation}, {users})")
        error_messages = []

        # validate the object
        if not users:
            error_messages.append('Users is required!')

        for user in users:
            self.validate(operation, user)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def register(self, modelObject: User) -> User:
        """Crates a new user"""
        logger.debug(f"+register({modelObject})")
        self.validate(SchemaOperation.CREATE, modelObject)
        if self.existsByFilter({"email": modelObject.email}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"User '{modelObject.email}' is already registered!")

        # load user's email address
        roleService = RoleService()
        roleModel = roleService.findByFilter({"name": "Owner"})
        logger.debug(f"roleModel={roleModel}")
        schemaObject = UserMapper.fromModel(modelObject)
        schemaObject = self.userRepository.save(schemaObject)
        if schemaObject and schemaObject.id is None:
            schemaObject = self.userRepository.findByFilter({"name": schemaObject.name})

        # persist user's security
        passwordHashCode = HashUtils.hashCode(modelObject.password)
        logger.debug(f"modelObject.password={modelObject.password}, passwordHashCode={passwordHashCode}")
        saltHashCode, hashCode = HashUtils.hashCodeWithSalt(passwordHashCode)
        logger.debug(f"saltHashCode={saltHashCode}, hashCode={hashCode}")
        # TODO: Capture platform value form user-agent
        userSecuritySchema = UserSecuritySchema(platform="Service", salt=saltHashCode, hashed_auth_token=hashCode)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")
        schemaObject.user_security = userSecuritySchema
        userSecuritySchema = self.userRepository.save(userSecuritySchema)
        logger.debug(f"userSecuritySchema={userSecuritySchema}")

        modelObject = UserMapper.fromSchema(schemaObject)
        # user = User.model_validate(userSchema)

        logger.debug(f"-register(), modelObject={modelObject}")
        return modelObject

    def bulkCreate(self, users: List[User]) -> List[User]:
        """Crates a new user"""
        logger.debug(f"+bulkCreate({users})")
        results = []
        for user in users:
            result = self.register(user)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, user: User) -> User:
        """Updates the user"""
        logger.debug(f"+update({user})")
        # self.validate(SchemaOperation.UPDATE, user)
        # check record exists by id
        if not self.existsByFilter({"id": user.id}):
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, f"User doesn't exist!")

        userSchemas = self.userRepository.findByFilter({"id": user.id})
        userSchema = userSchemas[0]
        #  Person
        if user.email and userSchema.email != user.email:
            userSchema.email = user.email
        if user.first_name and userSchema.first_name != user.first_name:
            userSchema.first_name = user.first_name
        if user.last_name and userSchema.last_name != user.last_name:
            userSchema.last_name = user.last_name
        if user.birth_date and userSchema.birth_date != user.birth_date:
            userSchema.birth_date = user.birth_date
        #  User
        if user.user_name and userSchema.user_name != user.user_name:
            userSchema.user_name = user.user_name
        if user.admin and userSchema.admin != user.admin:
            userSchema.admin = user.admin
        if user.last_seen and userSchema.last_seen != user.last_seen:
            userSchema.last_seen = user.last_seen
        if user.avatar_url and userSchema.avatar_url != user.avatar_url:
            userSchema.avatar_url = user.avatar_url

        # userSchema = CompanyMapper.fromModel(oldRole)
        self.userRepository.update(userSchema)
        # userSchema = self.userRepository.update(mapper=UserSchema, mappings=[userSchema])
        userSchema = self.userRepository.findByFilter({"id": user.id})[0]
        user = UserMapper.fromSchema(userSchema)
        logger.debug(f"-update(), user={user}")
        return user

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.userRepository.delete(filter)
        else:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "User doesn't exist!")

        logger.debug(f"-delete()")
