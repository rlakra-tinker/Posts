#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException
from framework.http import HTTPStatus
from framework.model import ErrorModel
from framework.service import AbstractService
from globals import connector
from rest.role.model import Role
from rest.role.repository import RoleRepository
from rest.role.schema import RoleSchema

logger = logging.getLogger(__name__)


class RoleService(AbstractService):

    def __init__(self):
        logger.debug("RoleService()")
        self.repository = RoleRepository(engine=connector.engine)
        self.validation_errors: Optional[List[ErrorModel]] = None

    def hasError(self) -> bool:
        """Returns true if any errors otherwise false"""
        return self.errors is not None

    def getErrors(self):
        return self.errors

    def addError(self, instance: ErrorModel):
        """Adds an object into the list of errors"""
        logger.debug(f"+addError(), instance={instance}")
        if self:
            self.errors = []

        self.errors.append(instance)
        logger.debug(f"-addError(), errors={self.errors}")

    def addErrors(self, instances: List[ErrorModel]):
        """Adds an object into the list of errors"""
        logger.debug(f"+addErrors(), instances={instances}")
        if not self.hasError():
            self.errors = []

        if instances and len(instances) > 0:
            self.errors.extend(instances)

        logger.debug(f"-addErrors(), errors={self.errors}")

    def validate(self, role: Role) -> None:
        logger.debug(f"+validate({role})")
        error_messages = []

        # validate the object
        if not role:
            error_messages.append('Role is required!')

        # validate the required fields
        if not role.name:
            error_messages.append('Role name is required!')

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    def validates(self, roles: List[Role]) -> None:
        logger.debug(f"+validates({roles})")
        error_messages = []

        # validate the object
        if not roles:
            error_messages.append('Roles is required!')

        for role in roles:
            self.validate(role)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, role: Role) -> Role:
        """Crates a new role"""
        logger.debug(f"+create({role})")
        roleSchema = self.repository.findByName(role.name)
        logger.debug(f"roleSchema={roleSchema}")
        # old_role = self.repository.find_by_name(role.name)
        # current_app.logger.debug(f"old_role={old_role}")
        if roleSchema:
            # raise ValueError(f"[{role.name}] role already exists!")
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{role.name}] role already exists!")

        # role = self.repository.create(role)
        roleSchema = self.fromModel(role)
        roleSchema = self.repository.save(roleSchema)
        if roleSchema and roleSchema.id is None:
            roleSchema = self.repository.findByName(role.name)

        role = self.fromSchema(roleSchema)
        # role = Role.model_validate(roleSchema)

        logger.debug(f"-create(), role={role}")
        return role

    def createBatch(self, roles: List[Role]) -> List[Role]:
        """Crates a new role"""
        logger.debug(f"+createBatch({roles})")
        results = []
        for role in roles:
            result = self.create(role)
            results.append(result)

        logger.debug(f"-createBatch(), results={results}")
        return results

    def find_all(self, filters) -> List[Optional[Role]]:
        logger.debug(f"find_all({filters})")
        return self.repository.filter(filters)

    def fromSchema(self, roleSchema: RoleSchema) -> Role:
        return Role(id=roleSchema.id, name=roleSchema.name, active=roleSchema.active, created_at=roleSchema.created_at,
                    updated_at=roleSchema.updated_at)

    def fromModel(self, role: Role) -> RoleSchema:
        return RoleSchema(id=role.id, name=role.name, active=role.active, created_at=role.created_at,
                          updated_at=role.updated_at)

    def findAll(self, filters: Dict[str, Any]) -> List[Optional[Role]]:
        logger.debug(f"+findAll({filters})")
        roleSchemas = self.repository.findAll(filters)
        logger.debug(f"roleSchemas => type={type(roleSchemas)}, values={roleSchemas}")
        roleModels = []
        for roleSchema in roleSchemas:
            logger.debug(f"roleSchema type={type(roleSchema)}, value={roleSchema}")
            roleModel = self.fromSchema(roleSchema)
            logger.debug(f"type={type(roleModel)}, roleModel={roleModel}")
            # roleModelValidate = Role.model_validate(roleSchema)
            # logger.debug(f"type={type(roleModelValidate)}, roleModelValidate={roleModelValidate}")
            roleModels.append(roleModel)

        # allRoles = [Role(**roleSchema) for roleSchema in roles]
        # logger.debug(f"Loaded [{len(allRoles)}] => allRows={allRoles}")
        logger.debug(f"-findAll(), roleModels={roleModels}")
        return roleModels

    def find_by_id(self, id: int) -> Role:
        return self.repository.find_by_id(id)

    def exists(self, id: int) -> bool:
        role = self.find_by_id(id)
        return True if role else False

    def update(self, role: Role) -> Role:
        if not role or not role.id:
            raise ValueError('The Role should have an ID!')

    def delete(self, id: int):
        pass
