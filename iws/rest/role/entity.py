#
# Author: Rohtash Lakra
#
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.entity import NamedEntity


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
