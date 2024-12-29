#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.service import AbstractService
from rest.role.model import Role
from rest.role.repository import RoleRepository
from rest.role.schema import RoleSchema

logger = logging.getLogger(__name__)


class RoleService(AbstractService):

    def __init__(self):
        logger.debug("RoleService()")
        self.repository = RoleRepository()

    # @override
    def fromSchema(self, roleSchema: RoleSchema) -> Role:
        # return Role(id=roleSchema.id, name=roleSchema.name, active=roleSchema.active, created_at=roleSchema.created_at,
        #             updated_at=roleSchema.updated_at)
        return Role(**roleSchema.toJSONObject())

    # @override
    def fromModel(self, role: Role) -> RoleSchema:
        # return RoleSchema(id=role.id, name=role.name, active=role.active, created_at=role.created_at,
        #                   updated_at=role.updated_at)
        return RoleSchema(**role.toJSONObject())

    def validate(self, operation: SchemaOperation, role: Role) -> None:
        logger.debug(f"+validate({operation}, {role})")
        # super().validate(operation, role)
        error_messages = []

        # validate the object
        if not role:
            error_messages.append("'Role' is not fully defined!")

        match operation.name:
            case SchemaOperation.CREATE.name:
                # validate the required fields
                if not role.name:
                    error_messages.append("Role 'name' is required!")

            case SchemaOperation.UPDATE.name:
                if not role.id:
                    error_messages.append("Role 'id' is required!")

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[AbstractModel]]:
        logger.debug(f"+findByFilter({filters})")
        roleSchemas = self.repository.findByFilter(filters)
        # logger.debug(f"roleSchemas => type={type(roleSchemas)}, values={roleSchemas}")
        roleModels = []
        for roleSchema in roleSchemas:
            # logger.debug(f"roleSchema type={type(roleSchema)}, value={roleSchema}")
            roleModel = self.fromSchema(roleSchema)
            # logger.debug(f"type={type(roleModel)}, roleModel={roleModel}")
            roleModels.append(roleModel)
            # roleModelValidate = Role.model_validate(roleSchema)
            # logger.debug(f"type={type(roleModelValidate)}, roleModelValidate={roleModelValidate}")

        logger.debug(f"-findByFilter(), roleModels={roleModels}")
        return roleModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        roleSchemas = self.repository.findByFilter(filters)
        result = True if roleSchemas else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, roles: List[Role]) -> None:
        logger.debug(f"+validates({operation}, {roles})")
        error_messages = []

        # validate the object
        if not roles:
            error_messages.append('Roles is required!')

        for role in roles:
            self.validate(operation, role)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, role: Role) -> Role:
        """Crates a new role"""
        logger.debug(f"+create({role})")
        if self.existsByFilter({"name": role.name}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{role.name}] role already exists!")

        # role = self.repository.create(role)
        roleSchema = self.fromModel(role)
        roleSchema = self.repository.save(roleSchema)
        if roleSchema and roleSchema.id is None:
            roleSchema = self.repository.findByFilter({"name": role.name})

        role = self.fromSchema(roleSchema)
        # role = Role.model_validate(roleSchema)

        logger.debug(f"-create(), role={role}")
        return role

    def bulkCreate(self, roles: List[Role]) -> List[Role]:
        """Crates a new role"""
        logger.debug(f"+bulkCreate({roles})")
        results = []
        for role in roles:
            result = self.create(role)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, role: Role) -> Role:
        """Updates the role"""
        logger.debug(f"+update({role})")
        # self.validate(SchemaOperation.UPDATE, role)
        # check record exists by id
        # if not self.existsByFilter({"id": role.id}):
        #     raise NoRecordFoundException(HTTPStatus.NOT_FOUND, f"Role doesn't exist!")
        roleSchemas = self.repository.findByFilter({"id": role.id})
        roleSchema = roleSchemas[0]
        if role.name and roleSchema.name != role.name:
            roleSchema.name = role.name

        if role.active and roleSchema.active != role.active:
            roleSchema.active = role.active

        if role.meta_data and roleSchema.meta_data != role.meta_data:
            roleSchema.meta_data = role.meta_data

        # roleSchema = self.fromModel(oldRole)
        self.repository.update(roleSchema)
        # roleSchema = self.repository.update(mapper=RoleSchema, mappings=[roleSchema])
        roleSchema = self.repository.findByFilter({"id": role.id})[0]
        role = self.fromSchema(roleSchema)
        logger.debug(f"-update(), role={role}")
        return role

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        if self.existsByFilter({"id": id}):
            self.repository.delete(id)
        else:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "Role doesn't exist!")

        logger.debug(f"-delete()")
