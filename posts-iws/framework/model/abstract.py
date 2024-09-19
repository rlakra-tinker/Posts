#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
import json
from typing import Optional, Dict
from pydantic import BaseModel, ConfigDict
from framework.http import HTTPStatus
from framework.utils import Utils


# AbstractModel
class AbstractModel(BaseModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True)

    def to_json(self):
        """Returns the JSON representation of this object."""
        # print(f"=====> {type(self)}")
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

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.get_id()}>"


# Named Entity
class NamedEntity(AbstractEntity):
    """NamedEntity used an entity with name in it"""
    name: str

    def get_name(self):
        return self.name

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.get_id()}, name={self.get_name()}>"


# Error Entity
class ErrorEntity(AbstractModel):
    """ErrorEntity represents the error object"""
    status_code: int = None
    message: str = None
    debug_info: Optional[Dict[str, object]] = None

    @staticmethod
    def build_error(http_status: HTTPStatus, message: str = None, exception: Exception = None,
                    is_critical: bool = False):
        if message is None:
            if exception is not None:
                message = str(exception)
            else:
                message = http_status.message

        # debug details
        debug_info = {}
        if is_critical and exception is not None:
            debug_info['exception'] = Utils.stack_trace(exception)
            return ErrorEntity(status_code=http_status.status_code, message=message, debug_info=debug_info)
        else:
            return ErrorEntity(status_code=http_status.status_code, message=message)

    def __repr__(self) -> str:
        return f"{type(self).__name__} <status_code={self.status_code}, message={self.message}, debug_info={self.debug_info}>"


class ResponseEntity(AbstractModel):
    """ErrorResponse represents error message"""
    status: int
    data: AbstractEntity = None
    error: ErrorEntity = None

    def has_error(self) -> bool:
        return self.error is not None

    def __repr__(self) -> str:
        return f"{type(self).__name__} <status={self.status}, data={self.data}, error={self.error}>"

    @staticmethod
    def build_response(http_status: HTTPStatus, entity: AbstractModel = None, message: str = None,
                       exception: Exception = None, is_critical: bool = False):
        response_entity = None
        if entity:
            if isinstance(entity, AbstractEntity):
                # set message, if missing
                if exception is not None:
                    error_entity = ErrorEntity.build_error(http_status, message, exception, is_critical)
                    response_entity = ResponseEntity(status=error_entity.status_code, data=entity, error=error_entity)
                else:
                    response_entity = ResponseEntity(status=http_status.status_code, data=entity)
            elif isinstance(entity, ErrorEntity):
                # set message, if missing
                if message is None:
                    if exception is not None:
                        message = str(exception)
                    else:
                        message = http_status.message

                # update entity's message and exception if missing
                if entity.message is None and message is not None:
                    entity.message = message

                # update debug details for critical errors
                if is_critical and exception is not None:
                    entity.debug_info['exception'] = stack_trace(exception)

                response_entity = ResponseEntity(status=http_status.status_code, error=entity)
        else:
            error_entity = ErrorEntity.build_error(http_status, message, exception, is_critical)
            response_entity = ResponseEntity(status=http_status.status_code, error=error_entity)

        return response_entity

    @staticmethod
    def build_response_json(http_status: HTTPStatus, entity: AbstractModel = None, message: str = None,
                            exception: Exception = None, is_critical: bool = False):
        return ResponseEntity.build_response(http_status, entity, message, exception, is_critical).to_json()
