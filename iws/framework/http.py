#
# Author: Rohtash Lakra
#
from flask import g, request, current_app
import uuid
from enum import auto, unique, Enum
from framework.enums import AutoUpperCase


def log_decorator(func):
    def wrapper(self, *args, **kwargs):

        def to_dictionary(data):
            if data is not None and type(data) not in HTTPUtils.__data_types:
                try:
                    # For variables of type api/objects/...
                    data = data.__dict__.copy()
                except Exception as ex:
                    print(f'Wrapper response conversion error! ex={ex}')
            return data

        if not g.get('execute_request'):
            g.execute_request = {
                'x-request-id': HTTPUtils.get_uuid(),
                'platform': g.user_agent.get('platform') if g.get('user_agent') else None
            }

        response = func(self, *args, **kwargs)

        # If want to disable logging decorator, add DISABLE_DECORATOR_LOGGING to application config feature_flags
        params = {}
        for idx, arg in enumerate(args):
            params[f'args[{idx}]'] = to_dictionary(arg)

        log_info = {
            **g.request_flow,
            'endpoint': request.full_path if request else None,
            'method': f'{self.__class__.__name__}.{func.__name__}()',
            'params': params,
            'kwargs': {**kwargs},
            'response': to_dictionary(response)
        }

        current_app.logger.info(f'[TRACEBACK] log_info={log_info}')

        return response

    return wrapper


@unique
class HTTPMethod(AutoUpperCase):
    """
    HTTP Methods

    REST APIs listen for HTTP methods like GET, POST, and DELETE to know which operations to perform on the web service’s resources.
    The HTTP method tells the API which action to perform on the resource.
    """
    GET = auto()  # Retrieve an existing resource.
    POST = auto()  # Create a new resource.
    PUT = auto()  # Update an existing resource.
    PATCH = auto()  # Partially update an existing resource.
    DELETE = auto()  # Delete a resource.

    @staticmethod
    def is_post(method: str) -> bool:
        return method and HTTPMethod.POST.name == method.upper()


@unique
class HTTPStatus(AutoUpperCase):
    """
    Status Code

    Once a REST API receives and processes an HTTP request, it will return an HTTP response.
    Included in this response is an HTTP status code. This code provides information about the results of the request.

    200	OK - The requested action was successful.
    201	Created	- A new resource was created.
    202	Accepted - The request was received, but no modification has been made yet.
    204	No Content - The request was successful, but the response has no content.
    400	Bad Request - The request was malformed.
    401	Unauthorized - The client is not authorized to perform the requested action.
    404	Not Found - The requested resource was not found.
    415	Unsupported Media Type - The request data format is not supported by the server.
    422	Unprocessable Entity - The request data was properly formatted but contained invalid or missing data.
    429 Too Many Requests -
    500	Internal Server Error - The server threw an error when processing the request.
    501 Not Implemented -
    502 Bad Gateway -
    503 Service Unavailable -
    504 Gateway Timeout -
    505 HTTP Version Not Supported -
    """

    OK = (200, 'OK')  # Retrieve an existing resource.
    CREATED = (201, 'Created')  # Retrieve an existing resource.
    ACCEPTED = (202, 'Accepted')  # Retrieve an existing resource.
    NO_CONTENT = (204, 'No Content')  # Retrieve an existing resource.
    BAD_REQUEST = (400, 'Bad Request')  # Retrieve an existing resource.
    UNAUTHORIZED = (401, 'Unauthorized')  # Retrieve an existing resource.
    NOT_FOUND = (404, 'Not Found')  # Retrieve an existing resource.
    UNSUPPORTED_MEDIA_TYPE = (415, 'Unsupported Media Type')  # Retrieve an existing resource.
    INVALID_DATA = (422, 'Unprocessable Entity')  # Retrieve an existing resource.
    TOO_MANY_REQUESTS = (429, 'Too Many Requests')  # Retrieve an existing resource.
    INTERNAL_SERVER_ERROR = (500, 'Internal Server Error')  # Retrieve an existing resource.

    def __new__(cls, status_code: int, message: str):
        obj = object.__new__(cls)
        obj.status_code = status_code
        obj.message = message
        return obj

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return f"{self.name} <{self.status_code}, {self.message}>"

    @staticmethod
    def by_status(status: int):
        for httpStatus in HTTPStatus:
            if httpStatus.status_code == status:
                return httpStatus

        return None

    @staticmethod
    def get_success_statuses() -> tuple:
        return list([HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT])

    @staticmethod
    def is_success_status(http_status) -> bool:
        return isinstance(http_status, HTTPStatus) and HTTPStatus.get_success_statuses().__contains__(http_status)


class HTTPUtils:
    """
    The HTTP handling utility.
    """

    __data_types = [str, dict, None, int, float, list]

    def __init__(self):
        self.method = None
        self.url = None

    @staticmethod
    def get_uuid() -> str:
        return uuid.uuid4().hex

    # @log_decorator
    def __execute(self, http_method: HTTPMethod, url: str):
        return ' '.join([http_method.name, url])

    def get(self, url: str):
        return self.__execute(HTTPMethod.GET, url)

    def post(self, url: str):
        return self.__execute(HTTPMethod.POST, url)

    def put(self, url: str):
        return self.__execute(HTTPMethod.PUT, url)

    def patch(self, url: str):
        return self.__execute(HTTPMethod.PATCH, url)

    def delete(self, url: str):
        return self.__execute(HTTPMethod.DELETE, url)
