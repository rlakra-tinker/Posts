#
# Author: Rohtash Lakra
#
from flask import current_app
from iws.framework.repository import AbstractRepository
from iws.rest.role.models import Role
from iws.framework.utils import Utils


class RoleRepository(AbstractRepository):

    def __init__(self):
        super(AbstractRepository, self).__init__()

    def create(self, role:Role) -> Role:
        """Inserts a new role"""
        current_app.logger.info(f"+create({role})")
        query = """
        INSERT INTO roles (name, active, created_at, updated_at) VALUES (?,?, ?, ?)
        """

        try:
            # current_app.logger.debug(f"query: {query}, query_values: {values}")
            cursor = self.execute(query, (role.name, role.active, role.created_at, role.updated_at))
            current_app.logger.debug(f"cursor: {cursor}, {cursor.rowcount}")
            if cursor.rowcount > 0:
                saved = self.find_by_name(role.name)
                current_app.logger.error(f"saved: {saved}")
                result = saved
        except Exception as ex:
            current_app.logger.error(ex)
            current_app.logger.error(Utils.stack_trace(ex))
            print(f"Role [{role.name}] already exists!")

        current_app.logger.info(f"-create(), result: {result}")
        return result

    def find_by_id(self, id) -> Role:
        return self.execute('SELECT * FROM roles WHERE id = ?', (id,)).fetchone()

    def exists(self, id: int) -> bool:
        current_app.logger.info(f"+exists({id})")
        role = self.find_by_id(id)
        current_app.logger.info(f"-exists(), role: {role}")
        return True if role else False

    def find_by_name(self, name) -> Role:
        current_app.logger.debug(f"+find_by_name({name})")
        cursor = super().execute('SELECT * FROM roles WHERE name = ?', params=(name,))
        current_app.logger.debug(f"cursor: {cursor}, {cursor.rowcount}")
        result = cursor.fetchone()
        current_app.logger.info(f"-find_by_name(), result: {result}")

    def update(self, role: Role) -> Role:
        if not role or not role.id:
            raise ValueError('The Role should have an ID!')

    def delete(self, id: int):
        pass
