import logging
import unittest

from rest.role.repository import RoleRepository
from rest.role.schema import RoleSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class RoleRepositoryTest(AbstractTestCase):
    """Unit-tests for Repository classes"""

    def setUp(self):
        """The setUp() method of the TestCase class is automatically invoked before each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+setUp()")
        super().setUp()

        # toString() test
        expected = "<class 'rest.role.repository.RoleRepository'>"
        self.assertEqual(expected, str(RoleRepository))

        # init object
        self.roleRepository = RoleRepository()
        logger.debug(f"roleRepository={self.roleRepository}")
        self.assertIsNotNone(self.roleRepository)
        expected = 'RoleRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(self.roleRepository))
        self.assertIsNotNone(self.roleRepository.get_engine())

        logger.debug("-setUp()")
        print()

    def tearDown(self):
        """The tearDown() method of the TestCase class is automatically invoked after each test, so it's an ideal place
        to insert common logic that applies to all the tests in the class"""
        logger.debug("+tearDown()")
        self.roleRepository = None
        self.assertIsNone(self.roleRepository)
        super().tearDown()
        logger.debug("-tearDown()")
        print()

    def test_create_role(self):
        logger.debug("+test_create_role()")
        # role
        role_json = {
            "name": "Test",
            "active": True,
            "meta_data": {
                "description": "Role's Metadata Description"
            }
        }

        roleSchema = RoleSchema(**role_json)
        logger.debug(f"roleSchema={roleSchema}")
        roleSchema = self.roleRepository.save(roleSchema)
        logger.debug(f"roleSchema={roleSchema}")
        self.assertIsNotNone(roleSchema.id)
        self.assertEqual(True, roleSchema.active)
        logger.debug("-test_create_role()")
        print()

    def test_create_role_with_permission(self):
        logger.debug("+test_create_role_with_permission()")
        # role
        role_json = {
            "name": "Test-2",
            "active": False,
            "meta_data": {
                "description": "Role's Metadata Description with Permission"
            }
        }

        roleSchema = RoleSchema(**role_json)
        logger.debug(f"roleSchema={roleSchema}")
        roleSchema = self.roleRepository.save(roleSchema)
        logger.debug(f"roleSchema={roleSchema}")
        self.assertIsNotNone(roleSchema.id)
        self.assertEqual(False, roleSchema.active)

        logger.debug("-test_create_role_with_permission()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
