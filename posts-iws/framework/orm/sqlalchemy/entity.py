#
# Author: Rohtash Lakra
# References: -
# - https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# - https://docs.sqlalchemy.org/en/20/orm/inheritance.html
#
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import func


class AbstractEntity(DeclarativeBase):
    """
     Define module-level constructs that will form the structures which we will be querying from the database.
     This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
     metadata that describes real SQL tables that exist, or will exist, in a particular database:

    The mapping starts with a base class, which above is called 'AbstractEntity', and is created by making a simple
    subclass against the 'DeclarativeBase' class.

    Individual mapped classes are then created by making subclasses of 'AbstractEntity'.
    A mapped class typically refers to a single particular database table, the name of which is indicated by using
    the '__tablename__' class-level attribute.

    Normally, when one would like to map two different subclasses to individual tables, and leave the base class
    unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
    the '__abstract__' indicator:
    """
    __abstract__ = True
    pass


class BaseEntity(AbstractEntity):
    """
    ID - Primary Key

    All ORM mapped classes require at least one column be declared as part of the primary key, typically by using
    the 'Column.primary_key' parameter on those 'mapped_column()' objects that should be part of the key.
    """
    __abstract__ = True

    # ID - Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # def __repr__(self) -> str:
    #     return f"BaseEntity <id={self.id!r}>"


class NamedEntity(BaseEntity):
    """
    name - name column
    """
    __abstract__ = True
    name: Mapped[str] = mapped_column(String(64))

    # def __repr__(self) -> str:
    #     return f"NamedEntity <id={self.id!r}, name={self.name!r}>"


class Role(NamedEntity):
    """
    [roles] Table
    """
    __tablename__ = "roles"

    # name: Mapped[str] = mapped_column(String(64))
    active: Mapped[bool] = True
    meta_data: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self) -> str:
        return f"Role <id={self.id!r}, name={self.name!r}, active={self.active!r}, meta_data={self.meta_data!r}, created_at={self.created_at}, updated_at={self.updated_at}>"


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
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    addresses: Mapped[List["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User <id={self.id!r}, user_name={self.user_name!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, admin={self.admin!r}, created_at={self.created_at}, updated_at={self.updated_at}>"


class UserRole(BaseEntity):
    """
    [user_roles] Table
    """
    __tablename__ = "user_roles"

    # foreign key to "roles.id" and "users.id" are added
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool] = True
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self) -> str:
        return f"UserRole <id={self.id!r}, role_id={self.role_id!r}, user_id={self.user_id!r}, active={self.active!r}, created_at={self.created_at}, updated_at={self.updated_at}>"


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
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self) -> str:
        return f"Address <id={self.id!r}, user_id={self.user_id!r}, street1={self.street1!r}, street2={self.street2!r}, city={self.city!r}, state={self.state!r}, country={self.country!r}, zip={self.zip!r}, created_at={self.created_at}, updated_at={self.updated_at}>"
