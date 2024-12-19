#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
import logging
from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, ConfigDict

from framework.http import HTTPStatus
from framework.utils import Utils

logger = logging.getLogger(__name__)


# AbstractModel
class AbstractPydanticModel(BaseModel):
    """AbstractPydanticModel is a base model for all other models inherit and provides basic configuration parameters.
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True)

    def to_json(self):
        """Returns the JSON representation of this object."""
        logger.debug(f"to_json() => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__}"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


class AbstractModel(AbstractPydanticModel):
    """AbstractModel is a base model for all other models inherit and provides basic configuration parameters.
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

    def _auditable(self) -> str:
        """Returns the string representation of this object"""
        return f"created_at={self.get_created_at()}, updated_at={self.get_updated_at()}>"

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, {self._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class NamedModel(AbstractModel):
    """NamedModel used an entity with a property called 'name' in it"""
    name: str

    def get_name(self):
        return self.name

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, name={self.get_name()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class ErrorModel(AbstractPydanticModel):
    """ErrorModel represents the error object"""
    status: int = None
    message: str = None
    debug_info: Optional[Dict[str, object]] = None

    def to_json(self):
        """Returns the JSON representation of this object."""
        logger.debug(f"to_json() => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    @staticmethod
    def buildError(http_status: HTTPStatus, message: str = None, exception: Exception = None,
                   is_critical: bool = False):
        """
        Builds the error object for the provided arguments
        Parameters:
            http_status: status of the request
            message: message of the error
            exception: exception for the error message
            is_critical: is error a critical error
        """
        logger.debug(f"buildError({http_status}, {message}, {exception}, {is_critical})")

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
            return ErrorModel(status=http_status.status_code, message=message, debug_info=debug_info)
        elif exception is not None:
            debug_info['exception'] = Utils.stack_trace(exception)
            return ErrorModel(status=http_status.status_code, message=message, debug_info=debug_info)
        else:
            return ErrorModel(status=http_status.status_code, message=message)

    @classmethod
    def jsonResponse(cls, http_status: HTTPStatus, message: str = None, exception: Exception = None,
                     is_critical: bool = False):
        return ErrorModel.buildError(http_status, message, exception, is_critical).to_json()

    def __str__(self):
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <status={self.status}, message={self.message}, debug_info={self.debug_info}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class ResponseModel(AbstractPydanticModel):
    """ResponseModel represents the response object"""
    status: int
    data: Optional[List[AbstractModel]] = None
    errors: Optional[List[ErrorModel]] = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <status={self.status}, data={self.data}, errors={self.errors}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)

    def to_json(self):
        """Returns the JSON representation of this object."""
        logger.debug(f"to_json() => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def add(self, entity: AbstractPydanticModel = None):
        """Adds an object into the list of data or errors"""
        logger.debug(f"add(), entity={entity}")
        if isinstance(entity, ErrorModel):
            if self.errors is None and entity:
                self.errors = []
            self.errors.append(entity)
        elif isinstance(entity, AbstractModel):
            if self.data is None and entity:
                self.data = []
            self.data.append(entity)
        else:
            logger.debug(f"Invalid entity:{entity}!")

    def addData(self, entities: List[AbstractModel] = None):
        """Adds an object into the list of data or errors"""
        logger.debug(f"addData(), entities={entities}")
        if entities:
            if self.data is None:
                self.data = []
            else:
                self.data.extend(entities)
        elif entities is not None and not entities:  # Emtpy list
            if self.data is None:
                self.data = []

    def addError(self, entities: List[ErrorModel] = None):
        """Adds an object into the list of data or errors"""
        logger.debug(f"addError(), entities={entities}")
        if entities:
            if self.errors is None:
                self.errors = []
            else:
                self.data.extend(entities)
        elif entities is not None and not entities:  # Emtpy list
            if self.errors is None:
                self.errors = []

    def hasError(self) -> bool:
        """Returns true if any errors otherwise false"""
        return self.errors is not None

    @classmethod
    def buildResponse(cls, http_status: HTTPStatus, entity: AbstractPydanticModel = None, message: str = None,
                      exception: Exception = None, is_critical: bool = False):
        logger.debug(f"+buildResponse({http_status}, {entity}, {message}, {exception}, {is_critical})")
        response = None
        if isinstance(entity, ErrorModel):  # check if an ErrorModel entity
            logger.debug(f"isinstance(entity, ErrorModel) => {isinstance(entity, ErrorModel)}")
            errorModel = ErrorModel.buildError(http_status, message, exception, is_critical)
            # update entity's message and exception if missing
            if not errorModel.message:
                errorModel.message = entity.message if entity.message else errorModel.message

            # build response and add errorModel in the list
            response = ResponseModel(status=http_status.status_code)
            response.add(errorModel)
        elif isinstance(entity, AbstractModel):
            logger.debug(f"isinstance(entity, AbstractModel) => {isinstance(entity, AbstractModel)}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            if HTTPStatus.is_success_status(http_status):
                # if not exception or not message:
                response.add(entity)
            else:
                response.add(ErrorModel.buildError(http_status, message, exception, is_critical))
        elif exception:
            logger.debug(f"elif exception => exception={exception}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            response.add(ErrorModel.buildError(http_status, message, exception, is_critical))
        elif not HTTPStatus.is_success_status(http_status):
            logger.debug(f"not HTTPStatus.is_success_status() => {HTTPStatus.is_success_status(http_status)}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            response.add(ErrorModel.buildError(http_status, message, exception, is_critical))
        else:
            logger.debug(f"else => ")

            response = ResponseModel(status=http_status.status_code)

        logger.debug(f"-buildResponse(), response={response}")
        return response

    @classmethod
    def jsonResponse(cls, http_status: HTTPStatus, entity: AbstractPydanticModel = None, message: str = None,
                     exception: Exception = None, is_critical: bool = False):
        return ResponseModel.buildResponse(http_status, [entity], message, exception, is_critical).to_json()
        # return ResponseEntity.response(http_status, entity, message, exception, is_critical).model_dump_json()

    @classmethod
    def jsonResponses(cls, entities: List[Optional[AbstractPydanticModel]] = []):
        responses = []
        for entity in entities:
            logger.debug(f"jsonResponses() => type={type(entity)}, object={str(entity)}, json={entity.to_json()}")
            responses.append(entity.to_json())

        return responses
