#
# Author: Rohtash Lakra
#
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.schema import NamedSchema


class Role(NamedSchema):
    """
    [roles] Table
    """
    __tablename__ = "roles"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = False
    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[str]] = mapped_column(String(256))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        # return f"Role <id={self.id!r}, name={self.name!r}, active={self.active!r}, meta_data={self.meta_data!r}, created_at={self.created_at}, updated_at={self.updated_at}>"
        return f"{type(self).__name__} <id={self.id!r}, name={self.name!r}, active={self.active!r}, meta_data={self.meta_data!r}, {self.auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
