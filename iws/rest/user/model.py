#
# Author: Rohtash Lakra
#
import logging
from dataclasses import field
from datetime import datetime
from typing import Optional, List

from framework.orm.pydantic.model import AbstractModel

logger = logging.getLogger(__name__)


class Person(AbstractModel):
    """Person contains properties specific to this object."""

    email: str = None
    first_name: str = None
    last_name: str = None
    birth_date: str | None = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, birth_date={self.birth_date!r}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class User(Person):
    """User contains properties specific to this object."""

    user_name: str = None
    password: str = None
    admin: bool | None = False
    last_seen: datetime | None = None
    avatar_url: str | None = None

    # roles: Optional[List["Role"]] = None
    addresses: Optional[List["Address"]] = field(default_factory=list)

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, email={}, user_name={}, first_name={}, last_name={}, admin={}, {}, addresses={}>"
                .format(self.getClassName(), self.id, self.email, self.user_name, self.first_name,
                        self.last_name, self.admin, self._auditable(), self.addresses))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Address(AbstractModel):
    """Address contains properties specific to this object."""

    user_id: int | None = None
    user: User = None
    street1: str = None
    street2: str | None = None
    city: str = None
    state: str = None
    country: str = None
    zip: str = None

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{self.getClassName()} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, {super()._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
