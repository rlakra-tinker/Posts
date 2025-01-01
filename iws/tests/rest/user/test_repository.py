import logging
import unittest

from rest.user.repository import UserRepository
from rest.user.schema import UserSchema, AddressSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def test_user_repository(self):
        logger.debug("+test_user_repository()")
        expected = "<class 'rest.user.repository.UserRepository'>"
        self.assertEqual(expected, str(UserRepository))

        # repository object

        repository = UserRepository()
        logger.debug(f"repository={repository}")
        self.assertIsNotNone(repository)
        expected = 'UserRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())

        # user
        userSchema = UserSchema(email="lakra@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-01-01",
                                user_name="lakra", password="password")

        logger.debug(f"userSchema={userSchema}")
        userSchema = repository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        logger.debug("-test_user_repository()")
        print()

    def test_user_repository_with_address(self):
        logger.debug("+test_user_repository_with_address()")
        expected = "<class 'rest.user.repository.UserRepository'>"
        self.assertEqual(expected, str(UserRepository))

        # repository object

        repository = UserRepository()
        logger.debug(f"repository={repository}")
        self.assertIsNotNone(repository)
        expected = 'UserRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())

        # user
        userSchema = UserSchema(email="lakra1@lakra.com", first_name="Roh", last_name="Lak", birth_date="2024-01-01",
                                user_name="lakra", password="password")
        # address
        address = AddressSchema(street1="123 Great St.", city="Hayward", state="California", country="United States",
                                zip="94544")
        userSchema.addresses = [address]

        logger.debug(f"userSchema={userSchema}")
        userSchema = repository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        logger.debug("-test_user_repository_with_address()")
        print()

    def test_user_repository_save(self):
        logger.debug("+test_user_repository_save()")
        repository = UserRepository()
        self.assertIsNotNone(repository)
        expected = 'UserRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())

        user_json = {
            "email": "test1@lakra.com",
            "first_name": "Roh",
            "last_name": "Lak",
            "birth_date": "2024-12-27",
            "user_name": "test1",
            "password": "password",
            "admin": "false",
            "addresses": [
                {
                    "street1": "123 Great St.",
                    "city": "Hayward",
                    "state": "California",
                    "country": "United States",
                    "zip": "94544"
                }
            ]
        }

        # user
        userSchema = UserSchema(**user_json)
        logger.debug(f"userSchema={userSchema}")
        userSchema = repository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertIsNotNone(userSchema.addresses)
        logger.debug("-test_user_repository_save()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
