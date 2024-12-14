#
# Author: Rohtash Lakra
#
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.entity import BaseEntity, NamedEntity


class Role(NamedEntity):
    """
    [roles] Table
    """
    __tablename__ = "roles"

    active: Mapped[bool] = True
    meta_data: Mapped[Optional[str]] = mapped_column(String(256))

    # created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Role <id={self.id!r}, name={self.name!r}, active={self.active!r}, meta_data={self.meta_data!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class User(BaseEntity):
    """
    [users] Table
    """
    __tablename__ = "users"

    user_name: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    admin: Mapped[bool] = False
    # created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"User <id={self.id!r}, user_name={self.user_name!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, admin={self.admin!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class UserRole(BaseEntity):
    """
    [user_roles] Table
    """
    __tablename__ = "user_roles"

    # foreign key to "roles.id" and "users.id" are added
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool] = True

    # created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"UserRole <id={self.id!r}, role_id={self.role_id!r}, user_id={self.user_id!r}, active={self.active!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Address(BaseEntity):
    """
    [addresses] Table
    """
    __tablename__ = "addresses"

    # foreign key to "users.id" is added
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    street1: Mapped[str] = mapped_column(String(64))
    street2: Mapped[Optional[str]] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    state: Mapped[str] = mapped_column(String(64))
    country: Mapped[str] = mapped_column(String(64))
    zip: Mapped[str] = mapped_column(String(64))

    # created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Address <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
