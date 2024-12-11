#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
from datetime import datetime
from typing import Optional, Dict, List

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
        # print(f"to_json() -> type: {type(self)}")
        return self.model_dump_json()

    def __str__(self):
        """Returns the string representation of this object"""
        return str(self)


# Abstract Entity
class AbstractEntity(AbstractModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    id: int = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


# Named Entity
class NamedEntity(AbstractEntity):
    """NamedEntity used an entity with name in it"""
    name: str

    def get_name(self):
        return self.name

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, name={self.get_name()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


# Error Entity
class ErrorEntity(AbstractModel):
    """ErrorEntity represents the error object"""
    status: int = None
    message: str = None
    debug_info: Optional[Dict[str, object]] = None

    @staticmethod
    def error(http_status: HTTPStatus, message: str = None, exception: Exception = None, is_critical: bool = False):
        """
        Builds the error object for the provided arguments
        Parameters:
            http_status: status of the request
            message: message of the error
            exception: exception for the error message
            is_critical: is error a critical error
        """
        # set message, if missing
        if message is None:
            if exception is not None:
                message = str(exception)
            elif http_status:
                message = http_status.message

        # debug details
        debug_info = {}
        if is_critical and exception is not None:
            debug_info['exception'] = Utils.stack_trace(exception)
            return ErrorEntity(status=http_status.status_code, message=message, debug_info=debug_info)
        elif exception is not None:
            debug_info['exception'] = Utils.stack_trace(exception)
            return ErrorEntity(status=http_status.status_code, message=message, debug_info=debug_info)
        else:
            return ErrorEntity(status=http_status.status_code, message=message)

    @staticmethod
    def error_response(http_status: HTTPStatus, message: str = None, exception: Exception = None,
                       is_critical: bool = False):
        return ErrorEntity.error(http_status, message, exception, is_critical).to_json()

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <status={self.status}, message={self.message}, debug_info={self.debug_info}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class ResponseEntity(AbstractModel):
    """ResponseEntity represents the response object"""
    status: int
    data: AbstractEntity = None
    errors: List[ErrorEntity] = None

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <status={self.status}, data={self.data}, errors={self.errors}>"

    def to_json(self):
        """Returns the JSON representation of this object."""
        print(f"to_json() -> type: {type(self)}")
        return self.model_dump_json()

    def has_error(self) -> bool:
        """Returns true if any errors otherwise false"""
        return self.errors is not None

    def __add_error(self, error: ErrorEntity = None):
        """Adds an error object into the list"""
        if self.errors is None and error:
            self.errors = []

        self.errors.append(error)

    @staticmethod
    def response(http_status: HTTPStatus, entity: AbstractModel = None, message: str = None,
                 exception: Exception = None, is_critical: bool = False):
        """
        Builds the response for the provided entity.
        Parameters:
            http_status: status of the request
            entity: an entity object
            message: information message
            exception: exceptions, if any
            is_critical: if the exception is considered a critical error
        """
        print(f"+response({http_status}, {entity}, {message}, {exception}, {is_critical})")
        response = None
        if entity:
            if isinstance(entity, ErrorEntity):  # check if an error entity
                # print(f"isinstance(entity, ErrorEntity) => {isinstance(entity, ErrorEntity)}")
                error = ErrorEntity.error(http_status, message, exception, is_critical)
                # update entity's message and exception if missing
                if not error.message:
                    error.message = entity.message if entity.message else error.message

                # build response and add error in the list
                response = ResponseEntity(status=http_status.status_code)
                response.__add_error(error)
            elif isinstance(entity, AbstractEntity):
                # print(f"isinstance(entity, AbstractEntity) => {isinstance(entity, AbstractEntity)}")
                response = ResponseEntity(status=http_status.status_code, data=entity)
                # build error response, if exception is provided
                if not HTTPStatus.is_success_status(http_status):
                    # if not exception or not message:
                    error = ErrorEntity.error(http_status, message, exception, is_critical)
                    response.__add_error(error)

        elif not exception:
            # print(f"not exception")
            response = ResponseEntity(status=http_status.status_code)
            # build error response, if exception is provided
            response.__add_error(ErrorEntity.error(http_status, message, exception, is_critical))
        else:
            # print(f"else")
            response = ResponseEntity(status=http_status.status_code)

        print(f"-response(), response: {response}")
        return response

    @staticmethod
    def build_response(http_status: HTTPStatus, entity: AbstractModel = None, message: str = None,
                       exception: Exception = None, is_critical: bool = False):
        return ResponseEntity.response(http_status, entity, message, exception, is_critical).to_json()
        # return ResponseEntity.response(http_status, entity, message, exception, is_critical).model_dump_json()

    @staticmethod
    def error_response(entities):
        responses = []
        for entity in entities:
            print(entity.to_json())
            responses.append(entity.to_json())

        return responses
