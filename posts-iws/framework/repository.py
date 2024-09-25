#
# Author: Rohtash Lakra
#
from flask import current_app
from webapp.globals import connector


class AbstractRepository(object):

    def execute(self, statement, params={}, many: bool = False):
        """Executes the query"""
        current_app.logger.info(f"execute({statement}, {params}, {many}), connector => {connector}")
        # print(f"execute({params}, {many}), connector => {connector}")
        connection = connector.get_connection()
        if (many):
            return connection.executemany(statement, params)
        else:
            return connection.execute(statement, params)
