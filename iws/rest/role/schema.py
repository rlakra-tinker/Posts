#
# Author: Rohtash Lakra
#
from typing import Optional

from sqlalchemy import PickleType, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from framework.orm.sqlalchemy.schema import BaseSchema, NamedSchema

"""
S = Subject = A person or automated agent
R = Role = Job function or title which defines an authority level
P = Permissions = An approval of a mode of access to a resource

A subject can have multiple roles.
A role can have multiple subjects.
A role can have many permissions.
A permission can be assigned to many roles.
An operation can be assigned to many permissions.
A permission can be assigned to many operations.
"""


class RoleSchema(NamedSchema):
    """ RoleSchema represents [roles] Table

    Role = Job function or title which defines an authority level
    A role can have multiple subjects.
    A role can have many permissions.
    """

    __tablename__ = "roles"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)
    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, active={}, meta_data={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.active,
                        self.meta_data,
                        self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class PermissionSchema(NamedSchema):
    """ PermissionSchema represents [roles] Table

    Permissions = An approval of a mode of access to a resource.
    A permission can be assigned to many roles.
    A permission can be assigned to many operations.
    """

    __tablename__ = "permissions"

    # not Optional[], therefore will be NOT NULL
    active: Mapped[bool] = mapped_column(unique=False, default=False)
    # Optional[], therefore will be NULL
    meta_data: Mapped[Optional[PickleType]] = mapped_column(JSON)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, name={}, active={}, meta_data={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.name,
                        self.active,
                        self.meta_data,
                        self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class RolePermissionSchema(BaseSchema):
    """ RolePermissionSchema represents [user_roles] Table """

    __tablename__ = "role_permissions"

    # foreign key to "roles.id" and "users.id" are added
    # not Optional[], therefore will be NOT NULL
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    # not Optional[], therefore will be NOT NULL
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))

    # Define the many-to-one relationship
    role: Mapped["RoleSchema"] = relationship("RoleSchema")
    permission: Mapped["PermissionSchema"] = relationship("PermissionSchema")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, role_id={}, permission_id={}, {}>"
                .format(self.getClassName(), self.id, self.role_id, self.permission_id, self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
