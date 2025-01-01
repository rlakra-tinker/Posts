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
        # return User(**userSchema.toJSONObject())
        logger.debug(f"+fromSchema({userSchema})")
        user = User(**userSchema.toJSONObject())
        if userSchema.addresses:
            addresses = []
            for entry in userSchema.addresses:
                address = Address(**entry.toJSONObject())
                # logger.debug(f"address={address}")
                addresses.append(address)

            # logger.debug(f"addresses={addresses}")
            user.addresses = addresses
            logger.debug(f"userSchema.addresses={user.addresses}")

        logger.debug(f"-fromSchema(), user={user}")
        return user

    @classmethod
    # @override
    def fromModel(self, user: User) -> UserSchema:
        logger.debug(f"+fromModel({user})")
        # return UserSchema(**user.toJSONObject())
        userSchema = UserSchema(**user.toJSONObject())
        if user.addresses:
            addresses = []
            for entry in user.addresses:
                address = AddressSchema(**entry.toJSONObject())
                # logger.debug(f"address={address}")
                addresses.append(address)

            # logger.debug(f"addresses={addresses}")
            userSchema.addresses = addresses
            # logger.debug(f"userSchema.addresses={userSchema.addresses}")

        logger.debug(f"-fromModel(), userSchema={userSchema}")
        return userSchema


class AddressMapper(Mapper):

    @classmethod
    def fromSchema(cls, addressSchema: AddressSchema) -> Address:
        return Address(**addressSchema.toJSONObject())

    @classmethod
    def fromModel(cls, addressModel: Address) -> AddressSchema:
        return AddressSchema(**addressModel.toJSONObject())
