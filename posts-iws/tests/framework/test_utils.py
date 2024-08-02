#
# Author: Rohtash Lakra
#
import unittest
import json

from tests.blueprints import app
from framework.utils import HTTPMethod, HTTPStatus


class UtilsTest(unittest.TestCase):

    logFileContents = False
    logKeys = False

    @classmethod
    def setUpClass(cls):
        # set app at class level
        cls.app = app
        # update app's config enableTesting=True
        cls.app.config.update({
            "enableTesting": True
        })

        # init client from app's client
        cls.client = app.test_client()

        # load json files
        with open('tests/data/app-configs.json', 'r') as app_config_file:
            # load key/values as options
            options = json.load(app_config_file)
            if cls.logFileContents:
                print(json.dumps(options))

            # store key/values to easy access
            for key, value in options.items():
                exec(f"cls.{key} = value")
                # print(f"{key} = {value}")
                if cls.logKeys:
                    print(key)

    def test_http_method(self):
        httpMethod = HTTPMethod.GET
        print(f"httpMethod={httpMethod}")
        self.assertEqual(HTTPMethod.GET, httpMethod)
        self.assertNotEqual(HTTPMethod.POST, httpMethod)

    def test_is_post(self):
        self.assertTrue(HTTPMethod.is_post("post"))
        self.assertTrue(HTTPMethod.is_post("Post"))
        self.assertTrue(HTTPMethod.is_post("POST"))
        self.assertTrue(HTTPMethod.is_post("PoST"))
        self.assertFalse(HTTPMethod.is_post("get"))

    def test_http_status(self):
        httpStatus = HTTPStatus.CREATED
        print(f"httpStatus={httpStatus}")
        self.assertEqual(HTTPStatus.CREATED, httpStatus)
        self.assertNotEqual(HTTPStatus.OK, httpStatus)

    def test_by_status(self):
        self.assertEqual(HTTPStatus.OK, HTTPStatus.by_status(200))
        self.assertEqual(HTTPStatus.CREATED, HTTPStatus.by_status(201))
        self.assertEqual(HTTPStatus.BAD_REQUEST, HTTPStatus.by_status(400))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, HTTPStatus.by_status(401))
        self.assertEqual(HTTPStatus.NOT_FOUND, HTTPStatus.by_status(404))
        self.assertEqual(HTTPStatus.TOO_MANY_REQUESTS, HTTPStatus.by_status(429))
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.by_status(500))
