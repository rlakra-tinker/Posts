#
# Author: Rohtash Lakra
#
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.schema import BaseSchema


class PersonSchema(BaseSchema):
    """[Person]"""
    __abstract__ = True

    # not Optional[], therefore will be NOT NULL
    email: Mapped[str] = mapped_column(String(128))
    # not Optional[], therefore will be NOT NULL
    first_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    last_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    birth_date: Mapped[datetime] = mapped_column(nullable=False)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class UserSchema(PersonSchema):
    """
    [users] Table
    """
    __tablename__ = "users"

    # not Optional[], therefore will be NOT NULL
    user_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    password: Mapped[str] = mapped_column(String(128))
    # not Optional[], therefore will be NOT NULL
    admin: Mapped[bool] = False

    # not Optional[], therefore will be NOT NULL
    last_seen: Mapped[datetime] = mapped_column(insert_default=func.now())
    # not Optional[], therefore will be NOT NULL
    avatar_url: Mapped[str] = mapped_column(String(128))

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    # addresses: Mapped[List["Role"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    # Optional[], therefore will be NULL
    # roles: Mapped[List["Role"]] = relationship(back_populates="role", cascade="all, delete-orphan")
    # roles: Mapped[List["UserRoleSchema"]] = relationship(back_populates="roles", cascade="all, delete-orphan", secondary="users")

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    # addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # Optional[], therefore will be NULL
    addresses: Mapped[Optional[List["AddressSchema"]]] = relationship(back_populates="user",
                                                                      cascade="all, delete-orphan")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, user_name={self.user_name!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, admin={self.admin!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class UserRoleSchema(BaseSchema):
    """
    [user_roles] Table
    """
    __tablename__ = "user_roles"

    # foreign key to "roles.id" and "users.id" are added
    # not Optional[], therefore will be NOT NULL
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = True

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, role_id={self.role_id!r}, user_id={self.user_id!r}, active={self.active!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class AddressSchema(BaseSchema):
    """
    [addresses] Table
    """
    __tablename__ = "addresses"

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # not Optional[], therefore will be NOT NULL
    user: Mapped["UserSchema"] = relationship(back_populates="addresses")

    # not Optional[], therefore will be NOT NULL
    street1: Mapped[str] = mapped_column(String(64))
    # Optional[], therefore will be NULL
    street2: Mapped[Optional[str]] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    city: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    state: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    country: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    zip: Mapped[str] = mapped_column(String(64))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
