#
# Author: Rohtash Lakra
#
from typing import Any
from typing import Mapping

from flask import current_app
from werkzeug.datastructures import MultiDict

from globals import connector


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
        if many:
            return connection.executemany(statement, params)
        else:
            return connection.execute(statement, params)

    def build_filters(self, filters, connector='AND', operators={}, return_tuple=False):
        current_app.logger.debug(f"+build_filters({filters}, {connector}, {operators}, {return_tuple})")
        filter_clause = ""
        query_params = {}
        if filters:
            query_fragments = []
            # check filter is type of multi-dictionary
            if isinstance(filters, MultiDict):
                # iterate each key
                for key in filters.keys():
                    values = filters.getlist(key)
                    # check values count
                    if len(values) > 1:
                        in_params = []
                        # iterate values
                        for index, value in enumerate(values):
                            unique_key = f'{key}_{index}'
                            in_params.append(f'%({unique_key})s')
                            query_params[unique_key] = value

                        query_fragments.append(f'{key} IN ({", ".join(in_params)})')
                    else:
                        unique_key = f'{key}_0'
                        operator = operators.get(key) if operators.get(key, None) else '='
                        query_fragments.append(f'{key}{operator}%({unique_key})s')
                        query_params[unique_key] = values[0]

            # check filters is type of mapping
            elif isinstance(filters, Mapping):
                # iterate each item of filters
                for index, (key, value) in enumerate(filters.items()):
                    # check value is type of list
                    if isinstance(value, list):
                        if not value:
                            query_fragments.append('FALSE')
                            continue

                        in_params = []
                        for index, list_value in enumerate(value):
                            unique_key = f'{key}_{index}'
                            in_params.append(f'%({unique_key})s')
                            query_params[unique_key] = list_value

                        query_fragments.append(f'{key} IN ({", ".join(in_params)})')
                    else:
                        operator = operators.get(key) if operators.get(key, None) else '='
                        query_fragments.append(f'{key}{operator}%({key})s')
                        query_params[key] = value
            else:
                raise ValueError('The "query_params" must be either dictionary or MultiDict!')
            filter_clause = f' {connector} '.join(query_fragments)

        # return response
        if return_tuple:
            current_app.logger.debug(f"-build_filters(), filter_clause={filter_clause}, query_params={query_params}")
            return filter_clause, query_params
        else:
            current_app.logger.debug(f"-build_filters(), filter_clause={filter_clause}")
            filter_clause

    def where_clause(self, filters, connector='AND', operators={}):
        current_app.logger.debug(f"where_clause({filters}, {connector}, {operators})")
        filter_clause, query_params = self.build_filters(filters, connector, operators, return_tuple=True)
        return 'WHERE ' + filter_clause, query_params if filters else filter_clause

    def build_update_set_fields(self, update_json):
        update_keys = list(update_json.keys())
        update_fields = ''.join([update_key + '=%(' + update_key + ')s, ' for update_key in update_keys[0:-1]]) + \
                        update_keys[-1] + '=%(' + update_keys[-1] + ')s'

        return 'SET ' + update_fields
