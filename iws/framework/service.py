#
# Author: Rohtash Lakra
#
import logging
from abc import abstractmethod
from typing import List, Optional, Dict, Any

from framework.model import AbstractModel
from framework.orm.sqlalchemy.schema import BaseSchema, SchemaOperation

logger = logging.getLogger(__name__)


class AbstractService(object):
    """
    An abstract service for all other services inherits.
    """

    def __init__(self):
        logger.debug("AbstractService()")
        pass

    @abstractmethod
    def fromSchema(self, baseSchema: BaseSchema) -> AbstractModel:
        logger.debug(f"fromSchema({baseSchema})")
        pass

    @abstractmethod
    def fromModel(self, baseModel: AbstractModel) -> BaseSchema:
        logger.debug(f"fromModel({baseModel})")
        pass

    @abstractmethod
    def validate(self, operation: SchemaOperation, baseModel: AbstractModel) -> None:
        logger.debug(f"validate({operation}, {baseModel})")
        pass

    @abstractmethod
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseSchema]]:
        logger.debug(f"findByFilter({filters})")
        pass

    @abstractmethod
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        logger.debug(f"existsByFilter({filters})")
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
