#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional

from flask import current_app

from framework.http import HTTPStatus
from framework.model import ErrorModel
from framework.service import AbstractService
from rest.role.model import Role
from rest.role.repository import RoleRepository

logger = logging.getLogger(__name__)


class RoleService(AbstractService):

    def __init__(self):
        logger.debug("RoleService()")
        self.repository = RoleRepository()

    def validate(self, role: Role):
        logger.debug(f"validate({role})")
        current_app.logger.debug(f"validate({role})")
        errors = []
        if role:
            if not role.name:
                errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'Role name is required!'))
        else:
            errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'Role is required!'))

        return errors

    def create(self, role: Role) -> Role:
        """Crates a new role"""
        logger.debug(f"+create({role})")
        current_app.logger.debug(f"+create({role})")
        old_role = self.repository.find_by_name(role.name)
        current_app.logger.debug(f"old_role: {old_role}")
        if old_role:
            raise ValueError("Role already exists with name!")

        role = self.repository.create(role)
        current_app.logger.debug(f"-create(), role: {role}")
        return role

    def find_all(self, filters) -> List[Optional[Role]]:
        logger.debug(f"find_all({filters})")
        return self.repository.filter(filters)

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
