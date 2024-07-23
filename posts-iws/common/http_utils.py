#
# Author: Rohtash Lakra
#
from enum import Enum, auto, unique


# Also, subclassing an enumeration is allowed only if the enumeration does not define any members.
# Auto name for the enum members
class AutoName(Enum):
    """
    Generate the next value when not given.

    name: the name of the member
    start: the initial start value or None
    count: the number of existing members
    last_value: the last value assigned or None
    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


# HttpMethod
@unique
class HttpMethod(AutoName):

    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
