#
# Author: Rohtash Lakra
#
from flask import current_app
from iws.framework.service import AbstractService
from iws.framework.model.abstract import ErrorEntity, ResponseEntity
from iws.framework.http import HTTPStatus
from iws.rest.role.repository import RoleRepository
from iws.rest.role.models import Role


class RoleService(AbstractService):

    def __init__(self):
        self.repository = RoleRepository()

    def validate(self, role: Role):
        current_app.logger.debug(f"validate({role})")
        errors = []
        if role:
            if not role.name:
                errors.append(ErrorEntity.error(HTTPStatus.INVALID_DATA, 'Role name is required!'))
        else:
            errors.append(ErrorEntity.error(HTTPStatus.INVALID_DATA, 'Role is required!'))

        return errors

    def create(self, role: Role) -> Role:
        """Crates a new role"""
        current_app.logger.debug(f"+create({role})")
        old_role = self.repository.find_by_name(role.name)
        current_app.logger.debug(f"old_role: {old_role}")
        if old_role:
            raise ValueError("Role already exists with name!")

        role = self.repository.create(role)
        current_app.logger.debug(f"-create(), role: {role}")
        return role

    def find_by_id(self, id:int) -> Role:
        return self.repository.find_by_id(id)

    def exists(self, id: int) -> bool:
        role = self.find_by_id(id)
        return True if role else False

    def update(self, role: Role) -> Role:
        if not role or not role.id:
            raise ValueError('The Role should have an ID!')

    def delete(self, id: int):
        pass
