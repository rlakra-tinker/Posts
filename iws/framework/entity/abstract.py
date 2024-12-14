#
# Author: Rohtash Lakra
# Reference(s):
#  - https://docs.pydantic.dev/latest/
#

"""
Abstract and reusable entities
"""
import json
from json import JSONEncoder


class GetClassAttr(type):
    """GetClassAttr returns the attribute of an object"""

    def __getitem__(cls, item):
        return getattr(cls, item)


class AbstractJSONHandler(JSONEncoder):
    """AbstractJSONHandler extends JSONEncoder"""

    # skip JSONEncoder properties
    _jsonEncKeys = ('skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'sort_keys', 'indent')

    def _skipDefaultKeys(self, entity):
        # skip JSONEncoder properties
        for key in AbstractJSONHandler._jsonEncKeys:
            if key in entity.__dict__:
                # print(f"key: {key}")
                entity.__delattr__(key)
        # print(f"entity.__dict__: {entity.__dict__}")

    def default(self, entity):
        """
        Implement this method in a subclass such that it returns
                a serializable object for ``o``, or calls the base implementation
                (to raise a ``TypeError``).
        """

        # print(f"default -> entity: {type(entity)}")
        if isinstance(entity, AbstractJSONHandler):
            # return self.model_dump()
            # return json.dumps(self)
            # obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
            #         allow_nan=True, cls=None, indent=None, separators=None,
            #         default=None, sort_keys=False, **kw
            # return
            # json.dumps(self, default=lambda entity: entity.__dict__, sort_keys=True, indent=2, separators =(",", ":"))
            # return json.dumps(self, default=lambda entity: entity.__dict__, indent=2)
            # return json.dumps(self, default=self.default(), sort_keys=True, indent=4)
            # return json.dumps(self, sort_keys=True, indent=4)

            # skip JSONEncoder properties
            self._skipDefaultKeys(entity)

            # tempObject = copy.deepcopy(entity)
            # for path in skipKeys:
            #     del reduce(op.getitem, path[:-1], tempObject)[path[-1]]
            #
            # return json.dumps(tempObject, default=lambda obj: obj.__dict__, indent=2)
            return json.dumps(entity, default=lambda obj: obj.__dict__, indent=2)

        # Let the base class default method raise the TypeError
        return super().default(entity)


# @dataclass
class AbstractEntity(AbstractJSONHandler):
    """AbstractEntity is the base entity of all other classes"""

    # __metaclass__ = GetClassAttr

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # def __getitem__(self, item):
    #     return self.__class__[item]

    def json(self):
        """Serialize this object as a JSON formatted stream to fp"""
        return self.default(self)

    @classmethod
    def from_json(cls, json_input):
        if isinstance(json_input, str):
            json_dict = json.loads(json_input)
            return cls(**json_dict)
        else:
            return cls(**json_input)

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__}"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# @dataclass
class BaseEntity(AbstractEntity):
    """BaseEntity is the base entity of all other classes"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None):
        super().__init__()
        self.id = id

    def get_id(self):
        """Get ID"""
        return self.id

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__} <id={self.get_id()}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# @dataclass
class NamedEntity(BaseEntity):
    """NamedEntity used an entity with name in it"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, id: int = None, name: str = None):
        super().__init__(id)
        self.name = name

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__} <id={self.get_id()}, name={self.name}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


# Error Entity
# @dataclass
class ErrorEntity(AbstractEntity):
    """ErrorEntity represents the error object"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, status, message: str, exception: Exception = None):
        super().__init__()
        self.status = status
        self.message = message
        self.exception = exception

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__} <status={self.status}, message={self.message}, exception={self.exception}>"
        # return f"{type(self)} <status={self.status}, message={self.message}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)


class ErrorResponse(AbstractEntity):
    """ErrorResponse represents error message"""

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, status, message: str = None, is_critical: bool = False, debug=None, exception: Exception = None):
        super().__init__()
        # current_app.logger.error('Headers:{}, Body:{}'.format(request.headers, request.get_data()))
        # current_app.logger.error('Message: {}'.format(message))

        if is_critical:
            if exception is not None:
                if debug is None:
                    debug = {}

                debug['exception'] = exception

            # current_app.logger.critical(
            #     message,
            #     exc_info=True,
            #     extra={'debug': debug} if debug is not None else {}
            # )

        self.error = ErrorEntity(status, message if message is not None else str(exception), exception)

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{type(self).__name__} <error={self.error}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)
