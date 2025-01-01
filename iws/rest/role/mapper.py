#
# Author: Rohtash Lakra
#
from framework.orm.mapper import Mapper
from rest.role.model import Role, Permission
from rest.role.schema import RoleSchema, PermissionSchema


class RoleMapper(Mapper):

    @classmethod
    def fromSchema(cls, roleSchema: RoleSchema) -> Role:
        return Role(**roleSchema.toJSONObject())

    @classmethod
    def fromModel(cls, roleModel: Role) -> RoleSchema:
        return RoleSchema(**roleModel.toJSONObject())


class PermissionMapper(Mapper):

    @classmethod
    def fromSchema(cls, permissionSchema: PermissionSchema) -> Permission:
        return Role(**permissionSchema.toJSONObject())

    @classmethod
    def fromModel(cls, permissionModel: Permission) -> PermissionSchema:
        return PermissionSchema(**permissionModel.toJSONObject())
