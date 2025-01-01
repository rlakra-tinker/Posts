#
# Author: Rohtash Lakra
#
import logging
from abc import abstractmethod

from framework.orm.pydantic.model import AbstractModel
from framework.orm.sqlalchemy.schema import BaseSchema

logger = logging.getLogger(__name__)


class Mapper:

    @staticmethod
    def isPydantic(instance: object) -> bool:
        """ Checks whether an object is pydantic. """
        return type(instance).__class__.__name__ == "ModelMetaclass"

    @classmethod
    @abstractmethod
    def fromSchema(cls, baseSchema: BaseSchema) -> AbstractModel:
        logger.debug(f"fromSchema({baseSchema})")
        return None

    @classmethod
    @abstractmethod
    def fromModel(cls, baseModel: AbstractModel) -> BaseSchema:
        logger.debug(f"fromModel({baseModel})")
        return None

    @classmethod
    def fromPydanticModel(cls, modelInstance: AbstractModel) -> BaseSchema:
        logger.debug(f"+fromPydanticModel({modelInstance})")
        classObject = cls()
        properties = dict(modelInstance)
        for key, value in properties.items():
            try:
                if Mapper.isPydantic(value):
                    value = getattr(cls, key).property.mapper.class_.fromPydanticModel(value)
                setattr(classObject, key, value)
            except AttributeError as e:
                raise AttributeError(e)

        logger.debug(f"-fromPydanticModel(), classObject={classObject}")
        return classObject

    @classmethod
    def parsePydanticModel(self, modelInstance: AbstractModel) -> BaseSchema:
        logger.debug(f"+parsePydanticModel({modelInstance})")
        if Mapper.isPydantic(modelInstance):
            try:
                converted_model = self.parsePydanticModel(dict(modelInstance))
                return modelInstance.Meta.orm_model(**converted_model)

            except AttributeError:
                model_name = modelInstance.__class__.__name__
                raise AttributeError(f"Error converting pydantic model: {model_name}.Meta.orm_model not specified!")

        elif isinstance(modelInstance, list):
            return [self.parsePydanticModel(model) for model in modelInstance]

        elif isinstance(modelInstance, dict):
            for key, model in modelInstance.items():
                modelInstance[key] = self.parsePydanticModel(model)

        logger.debug(f"-parsePydanticModel(), modelInstance={modelInstance}")
        return modelInstance

    @classmethod
    # @abstractmethod
    def fromSQLAlchemySchema(cls, baseSchema: BaseSchema) -> AbstractModel:
        logger.debug(f"fromSQLAlchemySchema({baseSchema})")
        return None

    @classmethod
    # @abstractmethod
    def parseSQLAlchemySchema(cls, baseSchema: BaseSchema) -> AbstractModel:
        logger.debug(f"parseSQLAlchemySchema({baseSchema})")
        return None
