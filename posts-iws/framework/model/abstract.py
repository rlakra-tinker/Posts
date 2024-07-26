#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#
from flask import current_app, g, request
from pydantic import BaseModel, ConfigDict
from framework.utils import HTTPStatus


# AbstractConfig
class AbstractModel(BaseModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True)


# Base Entity
# @dataclass
class AbstractEntity(AbstractModel):
    """
    A base model for all other models inherit and provides basic configuration parameters.
    """
    id: int = None

    def json(self):
        return self.model_dump()


# Named Entity
class NamedEntity(AbstractEntity):
    name: str


# Error Entity
# @dataclass
class ErrorEntity(AbstractModel):
    http_status: HTTPStatus
    message: str = None
    exception: Exception = None

    @staticmethod
    def get_error(status, message=None, is_critical=False, debug=None, exception: Exception = None):
        current_app.logger.error('Headers:{}, Body:{}'.format(request.headers, request.get_data()))
        current_app.logger.error('Message: {}'.format(message))

        if is_critical:
            if exception is not None:
                if debug is None:
                    debug = {}

                debug['exception'] = exception

            current_app.logger.critical(
                message,
                exc_info=True,
                extra={'debug': debug} if debug is not None else {}
            )

        error = ErrorEntity(http_status=status, message=message if message is not None else str(exception),
                            exception=exception)
        # TODO: FIX ME!
        # error_json = json.dumps(error, lambda o: o.__dict__)
        print(f"error_json:{error.json()}")

        return {
            'error': error.json()
        }

    def json(self):
        return self.model_dump()
