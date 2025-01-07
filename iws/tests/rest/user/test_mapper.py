import logging
import unittest

from rest.user.mapper import UserMapper, AddressMapper
from rest.user.model import User, Address
from rest.user.schema import UserSchema, AddressSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserMapperTest(AbstractTestCase):
    """Unit-tests for Mapper classes"""

    def test_user_mappers(self):
        logger.debug("+test_user_mappers()")
        expected = "<class 'rest.user.mapper.UserMapper'>"
        self.assertEqual(expected, str(UserMapper))

        expected = "<class 'rest.user.mapper.AddressMapper'>"
        self.assertEqual(expected, str(AddressMapper))
        logger.debug("-test_user_mappers()")
        print()

    def assertUserSchemaAndUser(self, userSchema: UserSchema, userModel: User):
        """Asserts the schema and model objects."""
        logger.debug(f"assertUserSchemaAndUser(), userSchema={userSchema}, userModel={userModel}")
        self.assertEqual(userSchema.id, userModel.id)
        self.assertEqual(userSchema.email, userModel.email)
        self.assertEqual(userSchema.first_name, userModel.first_name)
        self.assertEqual(userSchema.last_name, userModel.last_name)
        self.assertEqual(userSchema.birth_date, userModel.birth_date)
        self.assertEqual(userSchema.user_name, userModel.user_name)
        self.assertEqual(userSchema.admin, userModel.admin)
        self.assertEqual(userSchema.last_seen, userModel.last_seen)
        self.assertEqual(userSchema.avatar_url, userModel.avatar_url)

    def test_user_fromSchema(self):
        logger.debug("+test_user_fromSchema()")
        # create a user
        userSchema = UserSchema(email="userSchema@lakra.com", first_name="Roh", last_name="Lak",
                                birth_date="2024-12-27",
                                user_name="userSchema", password="password")
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)
        userModel = UserMapper.fromSchema(userSchema)
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)

        # validate objects
        self.assertUserSchemaAndUser(userSchema, userModel)
        logger.debug("-test_user_fromSchema()")
        print()

    def test_user_fromModel(self):
        logger.debug("+test_user_fromModel()")
        # create a user
        userModel = User(email="userModel@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name="userModel", password="password")
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)
        userSchema = UserMapper.fromModel(userModel)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)

        # validate objects
        self.assertUserSchemaAndUser(userSchema, userModel)
        logger.debug("-test_user_fromModel()")
        print()

    def assertAddressSchemaAndAddress(self, addressSchema: AddressSchema, address: Address):
        """Asserts the schema and model objects."""
        logger.debug(f"assertAddressSchemaAndAddress(), addressSchema={addressSchema}, address={Address}")
        self.assertEqual(addressSchema.id, address.id)
        self.assertEqual(addressSchema.street1, address.street1)
        self.assertEqual(addressSchema.city, address.city)
        self.assertEqual(addressSchema.state, address.state)
        self.assertEqual(addressSchema.country, address.country)
        self.assertEqual(addressSchema.zip, address.zip)

    def test_address_fromSchema(self):
        logger.debug("+test_address_fromSchema()")
        # create an address
        addressSchema = AddressSchema(street1="123 Test Dr.", city="Hayward", state="California",
                                      country="United States", zip="94544")
        logger.debug(f"addressSchema={addressSchema}")
        self.assertIsNotNone(addressSchema)
        addressModel = AddressMapper.fromSchema(addressSchema)
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)

        # validate objects
        self.assertAddressSchemaAndAddress(addressSchema, addressModel)
        logger.debug("-test_address_fromSchema()")
        print()

    def test_address_fromModel(self):
        logger.debug("+test_address_fromModel()")
        # create an address
        addressModel = Address(street1="123 Test Dr.", city="Hayward", state="California",
                               country="United States", zip="94544")
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)
        addressSchema = AddressMapper.fromModel(addressModel)
        logger.debug(f"addressSchema={addressSchema}")
        self.assertIsNotNone(addressSchema)

        # validate objects
        self.assertAddressSchemaAndAddress(addressSchema, addressModel)
        logger.debug("-test_address_fromModel()")
        print()

    def test_user_fromModel_with_address(self):
        logger.debug("+test_user_fromModel_with_address()")
        # Create user with address
        userModel = User(email="userModel@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-12-27",
                         user_name="userModel", password="password")
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel)

        # create address
        addressModel = Address(street1="123 Test Dr.", city="Hayward", state="California",
                               country="United States", zip="94544")
        logger.debug(f"addressModel={addressModel}")
        self.assertIsNotNone(addressModel)
        # Assign address to user
        userModel.addresses.append(addressModel)
        logger.debug(f"userModel={userModel}")
        self.assertIsNotNone(userModel.addresses)

        userSchema = UserMapper.fromModel(userModel)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema)

        self.assertUserSchemaAndUser(userSchema, userModel)
        self.assertIsNotNone(userSchema.addresses)
        self.assertIsNotNone(userSchema.addresses)
        self.assertEqual(1, len(userSchema.addresses))
        self.assertEqual(1, len(userSchema.addresses))

        # asset user's address
        self.assertAddressSchemaAndAddress(userSchema.addresses[0], addressModel)
        logger.debug("-test_user_fromModel_with_address()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
