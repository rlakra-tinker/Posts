#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
from flask import current_app, request
from pydantic import BaseModel, ConfigDict
from framework.utils import HTTPStatus


# AbstractModel
class AbstractModel(BaseModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True)

    def toJson(self):
        """Returns the JSON representation of this object."""
        return self.model_dump_json()

    def __str__(self):
        return self.__repr__()


# Abstract Entity
class AbstractEntity(AbstractModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    id: int = None

    def get_id(self):
        return self.id

    # def toJson(self):
    #     return self.model_dump_json()

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.id}>"


# Named Entity
class NamedEntity(AbstractEntity):
    """NamedEntity used an entity with name in it"""
    name: str

    def get_name(self):
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.get_id()}, name={self.name}>"


# Error Entity
class ErrorEntity(AbstractModel):
    """ErrorEntity represents the error object"""
    http_status: HTTPStatus = None
    message: str = None
    exception: Exception = None

    def get_http_status(self):
        return self.http_status

    def get_message(self):
        return self.message

    def get_exception(self):
        return self.exception

    def __repr__(self) -> str:
        return f"{type(self).__name__} <http_status={self.http_status}, message={self.message}, exception={self.exception}>"

    # def json(self):
    #     return self.model_dump()


class ErrorResponse(AbstractModel):
    """ErrorResponse represents error message"""
    error: ErrorEntity = None

    @staticmethod
    def get_error(cls, status, message: str = None, isCritical: bool = False, debug=None, exception: Exception = None):
        if isCritical:
            if exception is not None:
                if debug is None:
                    debug = {}
                debug['exception'] = exception

        return ErrorEntity(status, message if message is not None else str(exception), exception)

    def __repr__(self) -> str:
        return f"{type(self).__name__} <error={self.error}>"
