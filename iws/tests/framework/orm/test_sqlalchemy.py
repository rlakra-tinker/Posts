#
# Author: Rohtash Lakra
#

import json
import logging
import unittest
from datetime import datetime

from framework.orm.sqlalchemy.schema import DefaultJSONEncoder, RecursiveJSONEncoder
from rest.account.schema import UserSchema, AddressSchema
from rest.role.schema import RoleSchema
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class SqlAlchemyTest(AbstractTestCase):
    """Unit-tests for sqlalchemy"""

    def test_default_json_encoder(self):
        logger.debug("test_default_json_encoder")
        roleSchema = RoleSchema(name="TestRole", active=True)
        # jsonInstance = json.dumps(roleSchema, cls=sql_alchemy_encoder(), check_circular=False)
        role_json = json.dumps(roleSchema, cls=DefaultJSONEncoder)
        logger.debug(f"roleSchema={roleSchema}, role_json={role_json}")
        print()

    def test_json(self):
        logger.debug(f"+test_json()")
        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            # birth_date=datetime.now(),
            # last_seen=datetime.now(),
            addresses=[]
        )

        self.assertIsNotNone(user)
        user_json = user.to_json()
        self.assertIsNotNone(user_json)
        logger.debug(f"user={user}")
        logger.debug(f"user_json={user_json}")
        logger.debug(f"json={json.dumps(user_json)}")
        print()
        jsonUser = user.toJson()
        self.assertIsNotNone(jsonUser)
        logger.debug(f"user={user}, jsonUser={jsonUser}, json={json.dumps(jsonUser)}")
        logger.debug(f"-test_json()")

    def test_recursive_encoder(self):
        logger.debug(f"test_recursive_encoder()")
        address = AddressSchema(
            street1="123 Great Rd",
            city="Hayward",
            state="California",
            country="US",
            zip="94544"
        )
        self.assertIsNotNone(address)
        address_json = json.dumps(address, cls=RecursiveJSONEncoder)
        logger.debug(f"address={address}, address_json={address_json}")
        self.assertIsNotNone(address_json)

        print()
        user = UserSchema(
            user_name="roh@lakra.com",
            password="Roh",
            email="roh@lakra.com",
            first_name="Rohtash",
            last_name="Lakra",
            admin=True,
            addresses=[address],
        )

        self.assertIsNotNone(user)
        user_json = json.dumps(user, cls=RecursiveJSONEncoder)
        logger.debug(f"user={user}, user_json={user_json}")
        self.assertIsNotNone(user_json)


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
