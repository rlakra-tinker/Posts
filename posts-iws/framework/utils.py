#
# Author: Rohtash Lakra
#
from enum import auto, unique
from framework.enums import AutoName


@unique
class HTTPMethod(AutoName):
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
    def is_post(http_method: str) -> bool:
        return http_method and HTTPMethod.POST.name == http_method.upper()


@unique
class HTTPStatus(AutoName):
    """
    Status Code

    Once a REST API receives and processes an HTTP request, it will return an HTTP response.
    Included in this response is an HTTP status code. This code provides information about the results of the request.

    200	OK	The requested action was successful.
    201	Created	A new resource was created.
    202	Accepted	The request was received, but no modification has been made yet.
    204	No Content	The request was successful, but the response has no content.
    400	Bad Request	The request was malformed.
    401	Unauthorized	The client is not authorized to perform the requested action.
    404	Not Found	The requested resource was not found.
    415	Unsupported Media Type	The request data format is not supported by the server.
    422	Unprocessable Entity	The request data was properly formatted but contained invalid or missing data.
    429 Too Many Requests
    500	Internal Server Error	The server threw an error when processing the request.
    501 Not Implemented
    502 Bad Gateway
    503 Service Unavailable
    504 Gateway Timeout
    505 HTTP Version Not Supported

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
        pass

    def __repr__(self):
        return f"{self.name} <{self.status_code}, {self.message}>"

    def __str__(self):
        return f"{self.name} <{self.status_code}, {self.message}>"


print()
get_method = HTTPMethod.GET
print(get_method)
print()

status = HTTPStatus.CREATED
# print(f"status={status}, status_code={status.status_code}, message={status.message}")
print(status)
print()
