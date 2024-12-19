#
# Author: Rohtash Lakra
#

from typing import Optional, List

from framework.model import AbstractModel


class User(AbstractModel):
    role_id: int = None
    user_name: str = None
    password: str = None
    email: str = None
    first_name: str = None
    last_name: str = None
    password: str = None
    is_admin: bool = False
    addresses: Optional[List["Address"]] = []

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, user_name={self.user_name!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, admin={self.admin!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Address(AbstractModel):
    user_id: int = None
    street1: str = None
    street2: Optional[str] = None
    city: str = None
    state: str = None
    country: str = None
    zip: str = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
