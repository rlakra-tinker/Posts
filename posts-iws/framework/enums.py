#
# Author: Rohtash Lakra
#
from enum import Enum, unique


@unique
class AutoName(Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()

