#
# Author: Rohtash Lakra
#
from abc import abstractmethod


class AbstractService(object):
    """
    An abstract service for all other services inherits.
    """

    def __init__(self):
        pass

    def load(schema_class, json, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).load_and_not_raise(json)

    def validate(schema_class, json, only=None, exclude=[], partial=False, many=False):
        schema_class(only=only, exclude=exclude, partial=partial, many=many).validate_and_raise(json)

    def dump(schema_class, obj, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).dump(obj)

    # Returns the next ID of the account
    @abstractmethod
    def find_by_id(self, id: int):
        pass


class DataStore:

    def init(self, app):
        self.app = app

    @property
    def get_app(self):
        return self.app
