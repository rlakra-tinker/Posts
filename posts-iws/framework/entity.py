#
# Author: Rohtash Lakra
#
import json
from json import JSONEncoder, JSONDecoder
from dataclasses import dataclass

from flask import current_app, g, request


# Base Entity
@dataclass
class AbstractEntity(JSONEncoder):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None):
        super().__init__(self)
        self.id = id

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.id}>"

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def default(self, entity):
        return entity.__dict__


@dataclass
# Named Entity
class NamedEntity(AbstractEntity):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, name: str = None):
        super.__init__(self)
        self.name = name

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.id}, name={self.name}>"


# Error Entity
@dataclass
class ErrorEntity:

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

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

        error = ErrorEntity(status, message if message is not None else str(exception), exception)
        # TODO: FIX ME!
        # error_json = json.dumps(error, lambda o: o.__dict__)
        print(f"error_json:{error}")

        return {
            'error': error
        }

    def __init__(self, status, message: str, exception: Exception = None):
        self.status = status
        self.message = message
        self.exception = exception

    def __repr__(self) -> str:
        return f"{type(self).__name__} <status={self.status}, message={self.message}>"
