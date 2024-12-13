#
# Author: Rohtash Lakra
#
import os
from enum import Enum, unique, auto
from typing import Any


# Also, subclassing an enumeration is allowed only if the enumeration does not define any members.
# Auto name for the enum members
class BaseEnum(Enum):
    """Base Enum for all other Enums. For readability, add constants in Alphabetical order."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Generate the next value when not given.

        name: the name of the member
        start: the initial start value or None
        count: the number of existing members
        last_value: the last value assigned or None
        """

        return name

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.__class__.__name__} <{self.name}{'=' + str(self.value) if self.value else ''}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return self.__str__()

    @classmethod
    def names(cls):
        "Returns the list of enum name"
        names = []
        for member in cls:
            if member and member.name:
                names.append(member.name)

        return tuple(names)

    @classmethod
    def of_name(cls, name: str) -> Enum:
        "Returns the Service Request Type object based on request_type param"
        if name is not None:
            for member in cls:
                if member.name.lower() == name.lower():
                    return member

        return None

    @classmethod
    def values(cls):
        "Returns the list of enum values"
        values = []
        for member in cls:
            if member and member.value:
                values.append(member.value)

        return tuple(values)

    @classmethod
    def of_value(cls, value: Any) -> Enum:
        "Returns the Service Request Type object based on request_type param"
        if value is not None:
            for member in cls:
                if member.value == value:
                    return member

        return None

    @classmethod
    def equals(cls, enum_type: Enum, text: str) -> bool:
        "Returns true if the text is either equals to name or value of an enum otherwise false"
        if enum_type is None:
            raise ValueError('enum_type should provide!')
        if text is None:
            raise ValueError('text should provide!')

        return enum_type == cls.of_name(text) or enum_type == cls.of_value(text)


@unique
class AutoLowerCase(BaseEnum):
    """AutoNameLowerCase class converts names to lower-case letters"""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


@unique
class AutoUpperCase(BaseEnum):
    """AutoUpperCase class converts names to upper-case letters"""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        # print(f"_generate_next_value_={type(name)}")
        return name.upper()


@unique
class KeyEnum(AutoUpperCase):
    SQLALCHEMY = auto()
    APP_ENV = auto()
    DB_TYPE = auto()


@unique
class EnvType(BaseEnum):
    """EnvType class represents various supported env types"""

    DEVELOPMENT = auto()
    PRODUCTION = auto()
    STAGING = auto()
    TESTING = auto()

    @staticmethod
    def is_development(env_type: str) -> bool:
        """Returns true if DEVELOPMENT == env_type other false"""
        return EnvType.equals(EnvType.DEVELOPMENT, env_type)

    @staticmethod
    def is_production(env_type: str) -> bool:
        """Returns true if PRODUCTION == env_type other false"""
        return EnvType.equals(EnvType.PRODUCTION, env_type)

    @staticmethod
    def is_staging(env_type: str) -> bool:
        """Returns true if STAGING == env_type other false"""
        return EnvType.equals(EnvType.STAGING, env_type)

    @staticmethod
    def is_testing(env_type: str) -> bool:
        """Returns true if TESTING == env_type other false"""
        return EnvType.equals(EnvType.TESTING, env_type)

    @staticmethod
    def flask_env() -> str:
        """Returns the value of FLASK_ENV env variable value if set otherwise None."""
        return os.getenv("FLASK_ENV")
