#
# Author: Rohtash Lakra
#
import logging

from framework.orm.mapper import Mapper
from rest.user.model import User, Address
from rest.user.schema import UserSchema, AddressSchema

logger = logging.getLogger(__name__)


class UserMapper(Mapper):

    @classmethod
    # @override
    def fromSchema(self, userSchema: UserSchema) -> User:
        logger.debug(f"+fromSchema({userSchema})")
        user = User(**userSchema.toJSONObject())
        logger.debug(f"userSchema={userSchema}, userSchema.addresses={userSchema.addresses}")
        if userSchema.addresses:
            user.addresses = [AddressMapper.fromSchema(address) for address in
                              userSchema.addresses] if userSchema.addresses else None
        logger.debug(f"-fromSchema(), user={user}")
        return user

    @classmethod
    # @override
    def fromModel(self, user: User) -> UserSchema:
        logger.debug(f"+fromModel({user})")
        userSchema = UserSchema(**user.toJSONObject())
        logger.debug(f"user={user}, user.addresses={user.addresses}")
        if user.addresses:
            userSchema.addresses = [AddressMapper.fromModel(address) for address in
                                    user.addresses] if user.addresses else None
        logger.debug(f"-fromModel(), userSchema={userSchema}")
        return userSchema


class AddressMapper(Mapper):

    @classmethod
    def fromSchema(cls, addressSchema: AddressSchema) -> Address:
        # logger.debug(f"+fromSchema(), addressSchema={addressSchema}")
        return Address(**addressSchema.toJSONObject())

    @classmethod
    def fromModel(cls, addressModel: Address) -> AddressSchema:
        # logger.debug(f"+fromModel(), addressModel={addressModel}")
        return AddressSchema(**addressModel.toJSONObject())
