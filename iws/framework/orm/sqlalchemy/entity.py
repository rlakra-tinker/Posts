#
# Author: Rohtash Lakra
# References: -
# - https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# - https://docs.sqlalchemy.org/en/20/orm/inheritance.html
#
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


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


class BaseEntity(AbstractEntity):
    """
    ID - Primary Key

    All ORM mapped classes require at least one column be declared as part of the primary key, typically by using
    the 'Column.primary_key' parameter on those 'mapped_column()' objects that should be part of the key.
    """
    __abstract__ = True

    # ID - Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __init__(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def set_attrs(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

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
