#
# Author: Rohtash Lakra
#
import json
import unittest
from tests.blueprints import app


class AbstractTestCase(unittest.TestCase):
    """An AbstractTestCase class the parent class of all the test cases."""

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

