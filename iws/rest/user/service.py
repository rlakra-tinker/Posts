#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel
from framework.orm.repository import isPydantic
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.service import AbstractService
from rest.role.service import RoleService
from rest.user.model import User, Address
from rest.user.repository import UserRepository
from rest.user.schema import UserSchema, AddressSchema

logger = logging.getLogger(__name__)


class UserService(AbstractService):

    def __init__(self):
        logger.debug("UserService()")
        self.repository = UserRepository()

    # @override
    def fromSchema(self, userSchema: UserSchema) -> User:
        # return User(**userSchema.toJSONObject())
        logger.debug(f"+fromSchema({userSchema})")
        user = User(**userSchema.toJSONObject())
        if userSchema.addresses:
            addresses = []
            for entry in userSchema.addresses:
                address = Address(**entry.toJSONObject())
                logger.debug(f"address={address}")
                addresses.append(address)

            logger.debug(f"addresses={addresses}")
            user.addresses = addresses
            logger.debug(f"userSchema.addresses={user.addresses}")

        logger.debug(f"-fromSchema(), user={user}")
        return user

    # @override
    def fromModel(self, user: User) -> UserSchema:
        logger.debug(f"+fromModel({user})")
        # return UserSchema(**user.toJSONObject())
        userSchema = UserSchema(**user.toJSONObject())
        if user.addresses:
            addresses = []
            for entry in user.addresses:
                address = AddressSchema(**entry.toJSONObject())
                logger.debug(f"address={address}")
                addresses.append(address)

            logger.debug(f"addresses={addresses}")
            userSchema.addresses = addresses
            logger.debug(f"userSchema.addresses={userSchema.addresses}")

        logger.debug(f"-fromModel(), userSchema={userSchema}")
        return userSchema

    def parsePydanticModel(self, modelInstance: AbstractModel) -> UserSchema:
        if isPydantic(modelInstance):
            try:
                converted_model = self.parsePydanticModel(dict(modelInstance))
                return modelInstance.Meta.orm_model(**converted_model)

            except AttributeError:
                model_name = modelInstance.__class__.__name__
                raise AttributeError(f"Error converting pydantic model: {model_name}.Meta.orm_model not specified!")

        elif isinstance(modelInstance, list):
            return [self.parsePydanticModel(model) for model in modelInstance]

        elif isinstance(modelInstance, dict):
            for key, model in modelInstance.items():
                modelInstance[key] = self.parsePydanticModel(model)

        return modelInstance

    def validate(self, operation: SchemaOperation, user: User) -> None:
        logger.debug(f"+validate({operation}, {user})")
        # super().validate(operation, user)
        error_messages = []

        # validate the object
        if not user:
            error_messages.append("'User' is not fully defined!")

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

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"-validate(), {type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[AbstractModel]]:
        logger.debug(f"+findByFilter({filters})")
        userSchemas = self.repository.findByFilter(filters)
        # logger.debug(f"userSchemas => type={type(userSchemas)}, values={userSchemas}")
        roleModels = []
        for userSchema in userSchemas:
            # logger.debug(f"userSchema type={type(userSchema)}, value={userSchema}")
            userModel = self.fromSchema(userSchema)
            # logger.debug(f"type={type(userModel)}, userModel={userModel}")
            roleModels.append(userModel)

        logger.debug(f"-findByFilter(), roleModels={roleModels}")
        return roleModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        userSchemas = self.repository.findByFilter(filters)
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

    def register(self, user: User) -> User:
        """Crates a new user"""
        logger.debug(f"+register({user})")
        if self.existsByFilter({"email": user.email}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"User '{user.email}' is already registered!")

        # load user's email address
        roleService = RoleService()
        roleModel = roleService.findByFilter({"name": "Manager"})
        logger.debug(f"roleModel={roleModel}")
        userSchema = self.fromModel(user)
        # userSchema = self.parsePydanticModel(user)
        # userSchema = UserSchema.fromPydanticModel(user)
        userSchema = self.repository.save(userSchema)
        if userSchema and userSchema.id is None:
            userSchema = self.repository.findByFilter({"name": user.name})

        user = self.fromSchema(userSchema)
        # user = User.model_validate(userSchema)

        logger.debug(f"-register(), user={user}")
        return user

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

        userSchemas = self.repository.findByFilter({"id": user.id})
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

        # userSchema = self.fromModel(oldRole)
        self.repository.update(userSchema)
        # userSchema = self.repository.update(mapper=UserSchema, mappings=[userSchema])
        userSchema = self.repository.findByFilter({"id": user.id})[0]
        user = self.fromSchema(userSchema)
        logger.debug(f"-update(), user={user}")
        return user

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        filter = {"id": id}
        if self.existsByFilter(filter):
            self.repository.delete(filter)
        else:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "User doesn't exist!")

        logger.debug(f"-delete()")
