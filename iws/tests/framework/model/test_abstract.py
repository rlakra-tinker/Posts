#
# Author: Rohtash Lakra
#
from framework.model.abstract import AbstractModel, AbstractEntity, NamedEntity, ErrorEntity, ResponseEntity
from framework.http import HTTPStatus
from tests.framework.base import AbstractTestCase


class TestAbstract(AbstractTestCase):

    def test_abstract_model(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_model()")
        abstract_model = AbstractModel(id=1)
        print(f"abstract_model: {abstract_model}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_model, AbstractModel))
        self.assertFalse(isinstance(abstract_model, TestAbstract))
        self.assertTrue(issubclass(AbstractModel, object))
        self.assertFalse(issubclass(object, AbstractModel))
        print("-test_abstract_model()")
        print()

    def test_abstract_entity(self):
        """Tests an AbstractEntity object"""
        print("+test_abstract_entity()")
        abstract_entity = AbstractEntity(id=1)
        print(f"abstract_entity: {abstract_entity}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_entity, AbstractEntity))
        self.assertFalse(isinstance(abstract_entity, TestAbstract))
        self.assertTrue(issubclass(AbstractEntity, object))
        self.assertFalse(issubclass(object, AbstractEntity))
        print("-test_abstract_entity()")
        print()

    def test_named_entity(self):
        """Tests an NamedEntity object"""
        print("+test_named_entity()")
        named_entity = NamedEntity(id=10, name="Roh")
        print(f"named_entity: {named_entity}")

        # valid object and expected results
        self.assertEqual(10, named_entity.get_id())
        self.assertNotEqual(2, named_entity.get_id())

        self.assertTrue(isinstance(named_entity, AbstractEntity))
        self.assertTrue(isinstance(named_entity, NamedEntity))
        self.assertFalse(isinstance(named_entity, TestAbstract))
        self.assertTrue(issubclass(NamedEntity, AbstractEntity))
        self.assertFalse(issubclass(AbstractEntity, NamedEntity))
        print("-test_named_entity()")
        print()

    def test_error_entity(self):
        """Tests an ErrorEntity object"""
        print("+test_error_entity()")
        error_entity = ErrorEntity.error(http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                         message="Internal Server Error!")
        print(f"error_entity: {error_entity}")

        # valid object and expected results
        self.assertIsNotNone(error_entity)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.status_code, error_entity.status)
        self.assertEqual("Internal Server Error!", error_entity.message)
        self.assertNotEqual(HTTPStatus.INTERNAL_SERVER_ERROR.message, error_entity.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST, error_entity.status)

        self.assertTrue(isinstance(error_entity, AbstractModel))
        self.assertTrue(isinstance(error_entity, ErrorEntity))
        self.assertFalse(isinstance(error_entity, AbstractEntity))
        self.assertTrue(issubclass(ErrorEntity, object))
        self.assertTrue(issubclass(ErrorEntity, AbstractModel))
        self.assertFalse(issubclass(AbstractModel, ErrorEntity))
        print("-test_error_entity()")
        print()

    def test_entity(self):
        """Tests all entities object"""
        print("+test_entity()")
        entity_object = AbstractEntity(id=100)
        print(f"entity_object: {entity_object}")
        self.assertEqual(100, entity_object.get_id())
        self.assertNotEqual("Lakra", entity_object.get_id())
        entity_object_json = entity_object.to_json()
        print(f"entity_object_json: \n{entity_object_json}")
        self.assertEqual(entity_object_json, entity_object.to_json())

        entity_object = NamedEntity(id=1600, name="R. Lakra")
        print(f"entity_object: {entity_object}")
        self.assertEqual(1600, entity_object.get_id())
        self.assertEqual("R. Lakra", entity_object.name)
        self.assertNotEqual("Lakra", entity_object.get_id())
        entity_object_json = entity_object.to_json()
        print(f"entity_object_json: \n{entity_object_json}")
        self.assertEqual(entity_object_json, entity_object.to_json())

        # valid object and expected results
        self.assertTrue(isinstance(entity_object, NamedEntity))
        self.assertTrue(isinstance(entity_object, AbstractEntity))
        self.assertFalse(isinstance(entity_object, ErrorEntity))
        self.assertFalse(issubclass(object, AbstractEntity))

        errorEntity = ErrorEntity.error(http_status=HTTPStatus.BAD_REQUEST, message="Error")
        print(f"errorEntity: {errorEntity}")

        # valid object and expected results
        self.assertIsNotNone(errorEntity)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, errorEntity.status)
        self.assertEqual("Error", errorEntity.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST.message, errorEntity.message)
        self.assertNotEqual(HTTPStatus.OK, errorEntity.status)

        errorEntityJson = errorEntity.to_json()
        print(f"errorEntityJson: \n{errorEntityJson}")
        print("-test_entity()")
        print()

    def test_response_entity_success(self):
        """Tests an ResponseEntity object"""
        print("\n+test_response_entity_success()")
        named_entity = NamedEntity(id=1600, name="R. Lakra")
        response_entity = ResponseEntity.response(HTTPStatus.CREATED, named_entity)
        print(f"response_entity: {response_entity}")
        self.assertIsNotNone(response_entity)
        self.assertEqual(HTTPStatus.CREATED.status_code, response_entity.status)
        self.assertIsNotNone(response_entity.data)
        self.assertIsNone(response_entity.errors)
        self.assertFalse(response_entity.has_error())

        # build json response
        response_entity_json = ResponseEntity.build_response(HTTPStatus.CREATED, named_entity)
        self.assertIsNotNone(response_entity_json)
        print(f"response_entity_json: {response_entity_json}")
        print("-test_response_entity_success()")
        print()

    def test_response_entity_error(self):
        """Tests an ResponseEntity object"""
        print("\n+test_response_entity_error()")
        error_entity = ErrorEntity.error(http_status=HTTPStatus.BAD_REQUEST, message="Error")
        response = ResponseEntity.response(HTTPStatus.BAD_REQUEST, error_entity)
        print(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.has_error())
        self.assertIsNotNone(response.errors)

        # build json response
        response_entity_json = ResponseEntity.build_response(HTTPStatus.BAD_REQUEST, error_entity)
        self.assertIsNotNone(response_entity_json)
        print(f"response_entity_json: {response_entity_json}")
        print("-test_response_entity_error()")
        print()

    def test_build_response_with_critical(self):
        """Tests an ResponseEntity.build_response() object"""
        print("+test_build_response_with_critical()")

        try:
            named_entity = NamedEntity(id=1600, name="R. Lakra")
            raise ValueError("The name should be unique!")
        except ValueError as ex:
            response = ResponseEntity.response(HTTPStatus.INTERNAL_SERVER_ERROR, named_entity, exception=ex, is_critical=True)

        print(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.status_code, response.status)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.has_error())
        self.assertIsNotNone(response.errors)
        print(f"response.errors => {response.errors}")
        self.assertEqual("The name should be unique!", response.errors[0].message)

        # build json response
        response_entity_json = response.to_json()
        self.assertIsNotNone(response_entity_json)
        print(f"response_entity_json: {response_entity_json}")
        print("-test_build_response_with_critical()")
        print()
