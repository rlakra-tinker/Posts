#
# Author: Rohtash Lakra
#
from typing import Optional

from sqlalchemy import PickleType, JSON
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.schema import NamedSchema


class RoleSchema(NamedSchema):
    """ RoleSchema represents [roles] Table """

    __tablename__ = "roles"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)
    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
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
