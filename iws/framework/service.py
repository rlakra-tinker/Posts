#
# Author: Rohtash Lakra
#
from abc import abstractmethod
from typing import List, Optional, Dict, Any

from framework.model import AbstractModel
from framework.orm.sqlalchemy.schema import BaseSchema


class AbstractService(object):
    """
    An abstract service for all other services inherits.
    """

    def __init__(self):
        pass

    @abstractmethod
    def fromSchema(self, baseSchema: BaseSchema) -> AbstractModel:
        pass

    @abstractmethod
    def fromModel(self, baseModel: AbstractModel) -> BaseSchema:
        pass

    @abstractmethod
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseSchema]]:
        pass

    @abstractmethod
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        pass

    def load(schema_class, json, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).load_and_not_raise(json)

    def validate(schema_class, json, only=None, exclude=[], partial=False, many=False):
        schema_class(only=only, exclude=exclude, partial=partial, many=many).validate_and_raise(json)

    def dump(schema_class, obj, only=None, exclude=[], partial=False, many=False):
        return schema_class(only=only, exclude=exclude, partial=partial, many=many).dump(obj)


class DataStore:

    def init(self, app):
        self.app = app

    @property
    def get_app(self):
        return self.app
