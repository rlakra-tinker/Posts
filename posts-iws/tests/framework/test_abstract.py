#
# Author: Rohtash Lakra
#
import json
import unittest
from tests.blueprints import app
from framework.entity.abstract import AbstractEntity, BaseEntity, NamedEntity, ErrorEntity, ErrorResponse


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


class TestAbstract(AbstractTestCase):

    def test_abstract_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_entity()")
        abstractEntity = AbstractEntity()
        print(f"abstractEntity: {abstractEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(abstractEntity, AbstractEntity))
        self.assertFalse(isinstance(abstractEntity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_abstract_entity()")

    def test_base_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_base_entity()")
        baseEntity = BaseEntity(1)
        print(f"baseEntity: {baseEntity}")

        # valid object and expected results
        self.assertEqual(1, baseEntity.get_id())
        self.assertNotEqual(2, baseEntity.get_id())

        self.assertTrue(isinstance(baseEntity, AbstractEntity))
        self.assertFalse(isinstance(baseEntity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_base_entity()")

    def test_named_entity(self):
        """Tests an NamedEntity object"""
        print("+test_named_entity()")
        namedEntity = NamedEntity(1, "Roh")
        print(f"namedEntity: {namedEntity}")

        # valid object and expected results
        self.assertEqual(1, namedEntity.get_id())
        self.assertNotEqual(2, namedEntity.get_id())

        self.assertTrue(isinstance(namedEntity, AbstractEntity))
        self.assertTrue(isinstance(namedEntity, NamedEntity))
        self.assertFalse(isinstance(namedEntity, TestAbstract))
        self.assertTrue(issubclass(NamedEntity, AbstractEntity))
        self.assertFalse(issubclass(AbstractEntity, NamedEntity))
        print("-test_named_entity()")

    def test_error_entity(self):
        """Tests an ErrorEntity object"""
        print("+test_error_entity()")
        errorEntity = ErrorEntity(200, "Success")
        print(f"errorEntity: {errorEntity}")

        # valid object and expected results
        self.assertEqual(200, errorEntity.status)
        self.assertNotEqual(400, errorEntity.status)
        self.assertEqual("Success", errorEntity.message)
        self.assertIsNone(errorEntity.exception)

        self.assertTrue(isinstance(errorEntity, AbstractEntity))
        self.assertTrue(isinstance(errorEntity, ErrorEntity))
        self.assertFalse(isinstance(errorEntity, BaseEntity))
        self.assertTrue(issubclass(ErrorEntity, object))
        self.assertTrue(issubclass(ErrorEntity, AbstractEntity))
        self.assertFalse(issubclass(ErrorEntity, BaseEntity))
        print("-test_error_entity()")

    def test_entity(self):
        """Tests all entities object"""
        print("+test_entity()")
        entityObject = BaseEntity(100)
        print(f"entityObject: {entityObject}")
        self.assertEqual(100, entityObject.get_id())
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.json()
        print(f"entityObjectJson: \n{entityObjectJson}")
        self.assertEqual(entityObjectJson, entityObject.json())

        entityObject = NamedEntity(1600, "R. Lakra")
        print(f"entityObject: {entityObject}")
        self.assertEqual(1600, entityObject.get_id())
        self.assertEqual("R. Lakra", entityObject.name)
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.json()
        print(f"entityObjectJson: \n{entityObjectJson}")

        # valid object and expected results
        self.assertTrue(isinstance(entityObject, NamedEntity))
        self.assertTrue(isinstance(entityObject, AbstractEntity))
        self.assertFalse(isinstance(entityObject, ErrorEntity))
        self.assertFalse(issubclass(object, AbstractEntity))

        errorEntity = ErrorEntity(400, "Error")
        print(f"errorEntity: {errorEntity}")
        errorEntityJson = errorEntity.json()
        print(f"errorEntityJson: \n{errorEntityJson}")
        print("-test_entity()")

    def test_error_response(self):
        """Tests an ErrorResponse object"""
        print("+test_error_response()")
        errorResponse = ErrorResponse(400, "Invalid Input!")
        print(f"errorResponse: {errorResponse}")
        self.assertIsNotNone(errorResponse)
        self.assertIsNotNone(errorResponse.error)
        self.assertEqual(400, errorResponse.error.status)
        self.assertEqual("Invalid Input!", errorResponse.error.message)
        self.assertIsNone(errorResponse.error.exception)

        errorResponseJson = errorResponse.json()
        print(f"errorResponseJson: \n{errorResponseJson}")
        print("-test_error_response()")
