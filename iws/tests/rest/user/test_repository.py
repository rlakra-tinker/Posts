import logging
import unittest

from rest.user.repository import UserRepository
from rest.user.schema import UserSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class UserRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.user.repository.UserRepository'>"
        self.assertEqual(expected, str(UserRepository))

        # init object
        self.userRepository = UserRepository()
        logger.debug(f"userRepository={self.userRepository}")
        self.assertIsNotNone(self.userRepository)
        expected = 'UserRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.userRepository))
        self.assertIsNotNone(self.userRepository.get_engine())

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.userRepository = None
        self.assertIsNone(self.userRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_user(self):
        logger.debug("+test_create_user()")

        # user
        user_json = {
            "email": "user1@lakra.com",
            "first_name": "Roh",
            "last_name": "Lak",
            "birth_date": "2024-12-27",
            "user_name": "user1",
            "password": "password",
            "admin": False
        }
        userSchema = UserSchema(**user_json)
        logger.debug(f"userSchema={userSchema}")
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(False, userSchema.admin)
        logger.debug("-test_create_user()")
        print()

    def test_create_user_with_address(self):
        logger.debug("+test_create_user_with_address()")

        # user
        user_json = {
            "email": "user2@lakra.com",
            "first_name": "Roh",
            "last_name": "Lak",
            "birth_date": "2024-12-27",
            "user_name": "user2",
            "password": "password",
            "admin": True,
            "addresses": [
                {
                    "street1": "123 Test Dr.",
                    "city": "Hayward",
                    "state": "California",
                    "country": "United States",
                    "zip": "94544"
                }
            ]
        }
        userSchema = UserSchema(**user_json)
        logger.debug(f"userSchema={userSchema}")
        userSchema = self.userRepository.save(userSchema)
        logger.debug(f"userSchema={userSchema}")
        self.assertIsNotNone(userSchema.id)
        self.assertEqual(True, userSchema.admin)
        logger.debug("-test_create_user_with_address()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
