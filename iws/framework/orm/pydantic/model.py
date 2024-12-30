#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
import json
import logging
from datetime import datetime
from enum import unique, auto
from typing import Optional, Dict, List, Any

from pydantic import BaseModel, ValidationError, ConfigDict, model_validator, field_validator

from framework.enums import BaseEnum
from framework.exception import AbstractException, ValidationException, DuplicateRecordException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.utils import Utils

logger = logging.getLogger(__name__)


@unique
class Status(BaseEnum):
    """Enum for Status. For readability, add constants in Alphabetical order."""
    CREATED = auto()
    DELETED = auto()
    UPDATED = auto()


@unique
class SyncStatus(BaseEnum):
    """Enum for SyncStatus. For readability, add constants in Alphabetical order."""
    COMPLETED = auto()
    FAILED = auto()
    IGNORED = auto()
    PENDING = auto()
    SCHEDULED = auto()


# AbstractModel
class AbstractPydanticModel(BaseModel):
    """AbstractPydanticModel is a base model for all models inherit and provides basic configuration parameters."""
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True)

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{type(self).__name__} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def getAllFields(self, alias=False) -> list:
        # return list(self.schema(by_alias=alias).get("properties").keys())
        return list(self.model_json_schema(by_alias=alias).get("properties").keys())

    @classmethod
    def getClassFields(cls, by_alias=False) -> list[str]:
        field_names = []
        for key, value in cls.model_fields.items():
            if by_alias and value.alias:
                field_names.append(value.alias)
            else:
                field_names.append(key)

        return field_names

    def toJSONObject(self) -> Any:
        # return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        logger.debug(f"{type(self).__name__} => type={type(self)}, object={str(self)}")
        return self.model_dump(mode="json")

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__}"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


class AbstractModel(AbstractPydanticModel):
    """AbstractModel is a base model for all models inherit and provides basic configuration parameters."""

    id: int = None
    created_at: datetime = None
    updated_at: datetime = None

    # @root_validator()
    # def on_create(cls, values):
    #     logger.debug(f"on_create({values})")
    #     print("Put your logic here!")
    #     return values

    @classmethod
    @model_validator(mode="before")
    def pre_validator(cls, values):
        logger.debug(f"pre_validator({values})")
        return values

    @model_validator(mode="after")
    def post_validator(self, values):
        logger.debug(f"post_validator({values})")
        return self

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def _auditable(self) -> str:
        """Returns the string representation of this object"""
        return f"created_at={self.get_created_at()}, updated_at={self.get_updated_at()}>"

    def load_and_not_raise(self, data):
        try:
            return self.load(data)
        except ValidationError as ex:
            logger.error(f"load_and_not_raise() => Error:{ex.errors()}")
            # err = get_error(exception=None, msg=e.messages, status=422)
            # return abort(make_response(err, err.get('error').get('status')))

    def validate_and_raise(self, data):
        errors = self.validate(data)
        if errors:
            logger.error(f"validate_and_raise() => Error:{errors}")
            # err = get_error(exception=None, msg=errors, status=422)
            # return abort(make_response(err, err.get('error').get('status')))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, {self._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class NamedModel(AbstractModel):
    """NamedModel used an entity with a property called 'name' in it"""
    name: str

    @classmethod
    @model_validator(mode="before")
    def pre_validator(cls, values):
        logger.debug(f"pre_validator({values})")
        if "name" not in values:
            raise ValueError("The model 'name' should be provided!")

        return values

    @classmethod
    @field_validator('name')
    def name_validator(cls, value):
        logger.info(f"name_validator({value})")
        if value is None or len(value) == 0:
            raise ValueError("The model 'name' should not be null or empty!")

        return value

    @model_validator(mode="after")
    def post_validator(self, values):
        logger.debug(f"post_validator({values})")
        return self

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

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{type(self).__name__} => type={type(self)}, object={str(self)}")
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
    message: Optional[str] = None
    data: Optional[List[AbstractModel]] = None
    errors: Optional[List[ErrorModel]] = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{type(self).__name__} => type={type(self)}, object={str(self)}")
        jsonObjects = {field: getattr(self, field) for field in self.getAllFields()}
        # logger.debug(f"jsonObjects type={type(jsonObjects)}, jsonObjects={jsonObjects}")
        # parse list of data to json
        if jsonObjects['data']:
            jsonData = []
            for item in jsonObjects['data']:
                # logger.debug(f"entry type={type(item)}, item={item}, json={item.to_json()}")
                jsonData.append(json.loads(item.to_json()))

            jsonObjects['data'] = jsonData

        # parse list of errors to json
        if jsonObjects['errors']:
            jsonErrors = []
            for item in jsonObjects['errors']:
                # logger.debug(f"entry type={type(item)}, item={item}, json={item.to_json()}")
                jsonErrors.append(json.loads(item.to_json()))

            jsonObjects['errors'] = jsonErrors

        return jsonObjects

    def toJSONObject(self) -> Any:
        # return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        # return self.model_dump(mode="json", serialize_as_any=True)
        # return self.model_dump(mode="json")
        jsonObject = self.model_dump(mode="json")
        for entry in self.data:
            logger.debug(f"entry type={type(entry)}, object={entry}")

        jsonObject["data"] = self.data.model_dump(mode="json")
        jsonObject["errors"] = self.errors.model_dump(mode="json")

        return jsonObject

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <status={self.status}, data={self.data}, errors={self.errors}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)

    def addInstance(self, instance: AbstractPydanticModel = None):
        """Adds an object into the list of data or errors"""
        logger.debug(f"+addInstance({instance})")
        if isinstance(instance, ErrorModel):
            if self.errors is None and instance:
                self.errors = []

            self.errors.append(instance)

        elif isinstance(instance, AbstractModel):
            if self.data is None and instance:
                self.data = []

            self.data.append(instance)
        else:
            logger.debug(f"Invalid instance:{instance}!")

        logger.debug(f"-addInstance(), data={self.data}, errors={self.errors}")

    def addInstances(self, instances: List[AbstractPydanticModel] = None):
        logger.debug(f"+addInstances(), instances={instances}")
        for instance in instances:
            self.addInstance(instance)

        logger.debug(f"-addInstances()")

    def hasError(self) -> bool:
        """Returns true if any errors otherwise false"""
        return self.errors is not None

    @classmethod
    def buildResponse(cls, http_status: HTTPStatus, instance: AbstractPydanticModel = None, message: str = None,
                      exception: Exception = None, is_critical: bool = False):
        logger.debug(f"+buildResponse({http_status}, {instance}, {message}, {exception}, {is_critical})")
        if isinstance(instance, ErrorModel):  # check if an ErrorModel entity
            logger.debug(f"isinstance(entity, ErrorModel) => {isinstance(instance, ErrorModel)}")
            errorModel = ErrorModel.buildError(http_status, message, exception, is_critical)
            # update entity's message and exception if missing
            if not errorModel.message:
                errorModel.message = instance.message if instance.message else errorModel.message

            # build response and add errorModel in the list
            response = ResponseModel(status=http_status.status_code)
            response.addInstance(errorModel)
        elif isinstance(instance, AbstractModel):
            logger.debug(f"isinstance(entity, AbstractModel) => {isinstance(instance, AbstractModel)}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            if HTTPStatus.is_success_status(http_status):
                # if not exception or not message:
                response.addInstance(instance)
            else:
                response.addInstance(ErrorModel.buildError(http_status, message, exception, is_critical))
        elif exception:
            logger.debug(f"elif exception => type={type(exception)}, exception={exception}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(http_status, message, exception, is_critical))
        elif not HTTPStatus.is_success_status(http_status):
            logger.debug(f"not HTTPStatus.is_success_status() => {HTTPStatus.is_success_status(http_status)}")
            response = ResponseModel(status=http_status.status_code)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(http_status, message, exception, is_critical))
        else:
            logger.debug(f"else => ")
            response = ResponseModel(status=http_status.status_code)

        logger.debug(f"-buildResponse(), response={response}")
        return response

    @classmethod
    def buildResponseWithException(cls, exception: AbstractException):
        logger.debug(f"+buildResponseWithException() => type={type(exception)}")
        # build response and add errorModel in the list
        if isinstance(exception, ValidationException):  # check if an AbstractException entity
            logger.debug(f"ValidationException => {isinstance(exception, ValidationException)}")
            response = ResponseModel(status=exception.httpStatus.status_code)
            for message in exception.messages:
                response.addInstance(ErrorModel.buildError(http_status=exception.httpStatus, message=message))
        elif isinstance(exception, DuplicateRecordException):
            logger.debug(f"DuplicateRecordException => {isinstance(exception, DuplicateRecordException)}")
            response = ResponseModel(status=exception.httpStatus.status_code)
            response.addInstance(
                ErrorModel.buildError(http_status=exception.httpStatus, message=exception.messages[:-1]))
        elif isinstance(exception, NoRecordFoundException):
            logger.debug(f"NoRecordFoundException => {isinstance(exception, NoRecordFoundException)}")
            response = ResponseModel(status=exception.httpStatus.status_code)
            response.addInstance(
                ErrorModel.buildError(http_status=exception.httpStatus, message=exception.messages[:-1])
            )
            # response = ResponseModel.buildResponse(HTTPStatus.CONFLICT, message=str(exception))
        elif isinstance(exception, AbstractException):
            logger.debug(f"isinstance(exception, AbstractException) => {isinstance(exception, AbstractException)}")
            response = ResponseModel(status=exception.httpStatus.status_code)
            for message in exception.messages:
                response.addInstance(ErrorModel.buildError(http_status=exception.httpStatus, message=message))

            response = ResponseModel.buildResponse(HTTPStatus.CONFLICT, message=str(exception))
        elif isinstance(exception, Exception):
            logger.debug(f"isinstance(exception, Exception) => {isinstance(exception, Exception)}")
            response = ResponseModel(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            # build errorModel response, if exception is provided
            response.addInstance(ErrorModel.buildError(HTTPStatus.INTERNAL_SERVER_ERROR, message=str(exception)))

        logger.debug(f"-buildResponseWithException(), type={type(exception)} response={response}")
        return response

    @classmethod
    def jsonResponseWithException(cls, exception: AbstractException):
        logger.debug(f"+jsonResponseWithException({exception})")
        response = cls.buildResponseWithException(exception).to_json()
        logger.debug(f"-jsonResponseWithException(), response={response}")
        return response

    @classmethod
    def jsonResponse(cls, http_status: HTTPStatus, instance: AbstractPydanticModel = None, message: str = None,
                     exception: Exception = None, is_critical: bool = False):
        return ResponseModel.buildResponse(http_status, [instance], message, exception, is_critical).to_json()

    @classmethod
    def jsonResponses(cls, instances: List[Optional[AbstractPydanticModel]] = []):
        responses = []
        for entity in instances:
            logger.debug(f"jsonResponses() => type={type(entity)}, object={str(entity)}, json={entity.to_json()}")
            responses.append(entity.to_json())

        return responses