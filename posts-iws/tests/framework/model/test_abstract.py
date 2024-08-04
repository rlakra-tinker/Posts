#
# Author: Rohtash Lakra
#
from framework.model.abstract import AbstractModel, AbstractEntity, NamedEntity, ErrorEntity, ErrorResponse
from framework.utils import HTTPStatus
from tests.framework.utils import AbstractTestCase


class TestAbstract(AbstractTestCase):

    def test_abstract_model(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_model()")
        abstractModel = AbstractModel(id=1)
        print(f"abstractModel: {abstractModel}")

        # valid object and expected results
        self.assertTrue(isinstance(abstractModel, AbstractModel))
        self.assertFalse(isinstance(abstractModel, TestAbstract))
        self.assertTrue(issubclass(AbstractModel, object))
        self.assertFalse(issubclass(object, AbstractModel))
        print("-test_abstract_model()")

    def test_abstract_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_entity()")
        abstractEntity = AbstractEntity(id=1)
        print(f"abstractEntity: {abstractEntity}")

        # valid object and expected results
        self.assertTrue(isinstance(abstractEntity, AbstractEntity))
        self.assertFalse(isinstance(abstractEntity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_abstract_entity()")

    def test_named_entity(self):
        """Tests an NamedEntity object"""
        print("+test_named_entity()")
        namedEntity = NamedEntity(id=10, name="Roh")
        print(f"namedEntity: {namedEntity}")

        # valid object and expected results
        self.assertEqual(10, namedEntity.get_id())
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
        errorEntity = ErrorEntity(http_status=HTTPStatus.by_status(200), message="Success")
        print(f"errorEntity: {errorEntity}")

        # valid object and expected results
        self.assertEqual(HTTPStatus.OK, errorEntity.http_status)
        self.assertEqual(HTTPStatus.OK.status_code, errorEntity.http_status.status_code)
        self.assertEqual(HTTPStatus.OK.message, errorEntity.http_status.message)
        self.assertEqual("Success", errorEntity.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST, errorEntity.http_status)
        self.assertIsNone(errorEntity.exception)

        self.assertTrue(isinstance(errorEntity, AbstractModel))
        self.assertTrue(isinstance(errorEntity, ErrorEntity))
        self.assertFalse(isinstance(errorEntity, AbstractEntity))
        self.assertTrue(issubclass(ErrorEntity, object))
        self.assertTrue(issubclass(ErrorEntity, AbstractModel))
        self.assertFalse(issubclass(AbstractModel, ErrorEntity))
        print("-test_error_entity()")

    def test_entity(self):
        """Tests all entities object"""
        print("+test_entity()")
        entityObject = AbstractEntity(id=100)
        print(f"entityObject: {entityObject}")
        self.assertEqual(100, entityObject.get_id())
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.toJson()
        print(f"entityObjectJson: \n{entityObjectJson}")
        self.assertEqual(entityObjectJson, entityObject.toJson())

        entityObject = NamedEntity(id=1600, name="R. Lakra")
        print(f"entityObject: {entityObject}")
        self.assertEqual(1600, entityObject.get_id())
        self.assertEqual("R. Lakra", entityObject.name)
        self.assertNotEqual("Lakra", entityObject.get_id())
        entityObjectJson = entityObject.toJson()
        print(f"entityObjectJson: \n{entityObjectJson}")

        # valid object and expected results
        self.assertTrue(isinstance(entityObject, NamedEntity))
        self.assertTrue(isinstance(entityObject, AbstractEntity))
        self.assertFalse(isinstance(entityObject, ErrorEntity))
        self.assertFalse(issubclass(object, AbstractEntity))

        errorEntity = ErrorEntity(http_status=HTTPStatus.by_status(400), message="Error")
        print(f"errorEntity: {errorEntity}")

        # valid object and expected results
        self.assertEqual(HTTPStatus.BAD_REQUEST, errorEntity.http_status)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, errorEntity.http_status.status_code)
        self.assertEqual(HTTPStatus.BAD_REQUEST.message, errorEntity.http_status.message)
        self.assertEqual("Error", errorEntity.message)
        self.assertNotEqual(HTTPStatus.OK, errorEntity.http_status)
        self.assertIsNone(errorEntity.exception)

        errorEntityJson = errorEntity.toJson()
        print(f"errorEntityJson: \n{errorEntityJson}")
        print("-test_entity()")

    def test_error_response(self):
        """Tests an ErrorResponse object"""
        print("+test_error_response()")
        errorEntity = ErrorEntity(http_status=HTTPStatus.by_status(400), message="Invalid Input!")
        errorResponse = ErrorResponse(error=errorEntity)
        print(f"errorResponse: {errorResponse}")

        self.assertIsNotNone(errorResponse)
        self.assertIsNotNone(errorResponse.error)

        self.assertEqual(HTTPStatus.BAD_REQUEST, errorResponse.error.http_status)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, errorResponse.error.http_status.status_code)
        self.assertEqual(HTTPStatus.BAD_REQUEST.message, errorResponse.error.http_status.message)
        self.assertEqual("Invalid Input!", errorResponse.error.message)
        self.assertNotEqual(HTTPStatus.OK, errorResponse.error.http_status)
        self.assertIsNone(errorResponse.error.exception)

        errorResponseJson = errorResponse.toJson()
        print(f"errorResponseJson: \n{errorResponseJson}")
        print("-test_error_response()")
