#
# Author: Rohtash Lakra
#
from typing import Any
from flask import current_app
from iws.common.globals import connector


class RepositoryManager(object):
    """The repository manager"""

    def __init__(self):
        self.engines: dict = None

    def register_engine(self, type: str, engine: Any):
        """Registers the repository for the given type"""

        if self.engines is None:
            self.engines = {}

        self.engines[type] = engine

    def get_engine(self, type: str):
        """Returns the repository's engine for the given type"""
        return self.engines[type] if type else None

    def remove_engine(self, type: str) -> bool:
        """Removes the repository for the given type"""

        if not type:
            self.engines.pop('type', None)
            return True

        return False

    def execute(self):
        """Executes the repository"""
        pass


class AbstractRepository(object):
    """The abstract repository of all other classes"""

    def execute(self, statement, params={}, many: bool = False):
        """Executes the query"""
        current_app.logger.info(f"execute({statement}, {params}, {many}), connector => {connector}")
        # print(f"execute({params}, {many}), connector => {connector}")
        connection = connector.get_connection()
        if (many):
            return connection.executemany(statement, params)
        else:
            return connection.execute(statement, params)
