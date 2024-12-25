#
# Author: Rohtash Lakra
#
from typing import Optional

from sqlalchemy import PickleType, JSON
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.schema import NamedSchema


class RoleSchema(NamedSchema):
    """
    [roles] Table
    """
    __tablename__ = "roles"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = False
    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        # return f"{type(self).__name__} <id={self.id!r}, name={self.name!r}, active={self.active!r}, meta_data={self.meta_data!r}, {self.auditable()}>"
        return ("{} <id={}, name={}, active={}, meta_data={}, {}>"
                .format(type(self).__name__,
                        self.id,
                        self.name,
                        self.active,
                        self.meta_data,
                        self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
