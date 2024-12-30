#
# Author: Rohtash Lakra
#
import json
import logging

from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractPydanticModel, AbstractModel, NamedModel, ErrorModel, ResponseModel
from tests.base import AbstractTestCase

logger = logging.getLogger(__name__)


class TestPydanticModel(AbstractTestCase):

    def test_abstract_pydantic_model(self):
        """Tests an AbstractEntity object"""
        logger.debug("+test_abstract_pydantic_model()")
        abstract_model = AbstractPydanticModel(id=1)
        logger.debug(f"abstract_model={abstract_model}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_model, AbstractPydanticModel))
        self.assertFalse(isinstance(abstract_model, TestPydanticModel))
        self.assertTrue(issubclass(AbstractPydanticModel, object))
        self.assertFalse(issubclass(object, AbstractPydanticModel))

        logger.debug("-test_abstract_pydantic_model()")
        print()

    def test_getAllFields(self):
        """Tests an getAllFields() method"""
        logger.debug("+test_getAllFields()")
        named_model = NamedModel(id=16, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = ['id', 'created_at', 'updated_at', 'name']
        allFields = named_model.getAllFields()
        logger.debug(f"allFields={allFields}")
        self.assertIsNotNone(allFields)
        self.assertEqual(expected, allFields)

        logger.debug("-test_getAllFields()")
        print()

    def test_getClassFields(self):
        """Tests an getClassFields() method"""
        logger.debug("+test_getClassFields()")
        named_model = NamedModel(id=16, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = ['id', 'created_at', 'updated_at', 'name']
        classFields = NamedModel.getClassFields()
        logger.debug(f"classFields={classFields}")
        self.assertIsNotNone(classFields)
        self.assertEqual(expected, classFields)

        logger.debug("-test_getClassFields()")
        print()

    def test_model_json_schema(self):
        """Tests an model_json_schema() method"""
        logger.debug("+test_model_json_schema()")
        namedModel = NamedModel(id=16, name="Roh")
        logger.debug(f"namedModel={namedModel}")

        # valid object and expected results
        self.assertTrue(isinstance(namedModel, NamedModel))
        self.assertFalse(isinstance(namedModel, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, object))
        self.assertFalse(issubclass(object, NamedModel))

        expected = {'description': "NamedModel used an entity with a property called 'name' in it",
                    'properties': {'id': {'default': None, 'title': 'Id', 'type': 'integer'},
                                   'created_at': {'default': None, 'format': 'date-time', 'title': 'Created At',
                                                  'type': 'string'},
                                   'updated_at': {'default': None, 'format': 'date-time', 'title': 'Updated At',
                                                  'type': 'string'}, 'name': {'title': 'Name', 'type': 'string'}},
                    'required': ['name'], 'title': 'NamedModel', 'type': 'object'}
        modelJsonSchema = NamedModel.model_json_schema()
        logger.debug(f"modelJsonSchema={modelJsonSchema}")
        logger.debug(f"json -> modelJsonSchema={json.dumps(modelJsonSchema)}")
        self.assertIsNotNone(modelJsonSchema)
        self.assertEqual(expected, modelJsonSchema)

        expected = {'id': 16, 'created_at': None, 'updated_at': None, 'name': 'Roh'}
        modelDump = namedModel.model_dump(mode="json")
        logger.debug(f"modelDump={modelDump}")
        logger.debug(f"json -> modelDump={json.dumps(modelDump)}")
        self.assertIsNotNone(modelDump)
        self.assertEqual(expected, modelDump)

        logger.debug("-test_model_json_schema()")
        print()

    def test_abstract_model(self):
        """Tests an AbstractModel object"""
        logger.debug("+test_abstract_model()")
        abstract_model = AbstractModel(id=1)
        logger.debug(f"abstract_model={abstract_model}")

        # valid object and expected results
        self.assertTrue(isinstance(abstract_model, AbstractModel))
        self.assertFalse(isinstance(abstract_model, TestPydanticModel))
        self.assertTrue(issubclass(AbstractModel, object))
        self.assertFalse(issubclass(object, AbstractModel))

        logger.debug("-test_abstract_model()")
        print()

    def test_named_model(self):
        """Tests an NamedEntity object"""
        logger.debug("+test_named_model()")
        named_model = NamedModel(id=10, name="Roh")
        logger.debug(f"named_model={named_model}")

        # valid object and expected results
        self.assertEqual(10, named_model.get_id())
        self.assertNotEqual(2, named_model.get_id())

        self.assertTrue(isinstance(named_model, AbstractModel))
        self.assertTrue(isinstance(named_model, NamedModel))
        self.assertFalse(isinstance(named_model, TestPydanticModel))
        self.assertTrue(issubclass(NamedModel, AbstractModel))
        self.assertFalse(issubclass(AbstractModel, NamedModel))

        logger.debug("-test_named_model()")
        print()

    def test_error_model(self):
        """Tests an ErrorEntity object"""
        logger.debug("+test_error_model()")
        error_model = ErrorModel.buildError(http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                            message="Internal Server Error!")
        logger.debug(f"error_model={error_model}")

        # valid object and expected results
        self.assertIsNotNone(error_model)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.status_code, error_model.status)
        self.assertEqual("Internal Server Error!", error_model.message)
        self.assertNotEqual(HTTPStatus.INTERNAL_SERVER_ERROR.message, error_model.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST, error_model.status)

        self.assertTrue(isinstance(error_model, AbstractPydanticModel))
        self.assertTrue(isinstance(error_model, ErrorModel))
        self.assertFalse(isinstance(error_model, AbstractModel))
        self.assertTrue(issubclass(ErrorModel, object))
        self.assertTrue(issubclass(ErrorModel, AbstractPydanticModel))
        self.assertFalse(issubclass(AbstractPydanticModel, ErrorModel))

        logger.debug("-test_error_model()")
        print()

    def test_models(self):
        """Tests all entities object"""
        logger.debug("+test_models()")
        entity_object = AbstractModel(id=100)
        logger.debug(f"entity_object: {entity_object}")
        self.assertEqual(100, entity_object.get_id())
        self.assertNotEqual("Lakra", entity_object.get_id())
        entity_object_json = entity_object.to_json()
        logger.debug(f"entity_object_json: \n{entity_object_json}")
        self.assertEqual(entity_object_json, entity_object.to_json())

        entity_object = NamedModel(id=1600, name="R. Lakra")
        logger.debug(f"entity_object: {entity_object}")
        self.assertEqual(1600, entity_object.get_id())
        self.assertEqual("R. Lakra", entity_object.name)
        self.assertNotEqual("Lakra", entity_object.get_id())
        entity_object_json = entity_object.to_json()
        logger.debug(f"entity_object_json: \n{entity_object_json}")
        self.assertEqual(entity_object_json, entity_object.to_json())

        # valid object and expected results
        self.assertTrue(isinstance(entity_object, NamedModel))
        self.assertTrue(isinstance(entity_object, AbstractModel))
        self.assertFalse(isinstance(entity_object, ErrorModel))
        self.assertFalse(issubclass(object, AbstractModel))

        errorModel = ErrorModel.buildError(http_status=HTTPStatus.BAD_REQUEST, message="Error")
        logger.debug(f"errorModel={errorModel}")

        # valid object and expected results
        self.assertIsNotNone(errorModel)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, errorModel.status)
        self.assertEqual("Error", errorModel.message)
        self.assertNotEqual(HTTPStatus.BAD_REQUEST.message, errorModel.message)
        self.assertNotEqual(HTTPStatus.OK, errorModel.status)

        errorEntityJson = errorModel.to_json()
        logger.debug(f"errorEntityJson=\n{errorEntityJson}")
        logger.debug("-test_models()")
        print()

    def test_response_entity_success(self):
        """Tests an ResponseEntity object"""
        logger.debug("\n+test_response_entity_success()")
        named_entity = NamedModel(id=1600, name="R. Lakra")
        response_entity = ResponseModel.buildResponse(HTTPStatus.CREATED, named_entity)
        logger.debug(f"response_entity={response_entity}")
        self.assertIsNotNone(response_entity)
        self.assertEqual(HTTPStatus.CREATED.status_code, response_entity.status)
        self.assertIsNotNone(response_entity.data)
        self.assertIsNone(response_entity.errors)
        self.assertFalse(response_entity.hasError())

        # build json response
        response_entity_json = ResponseModel.jsonResponse(HTTPStatus.CREATED, named_entity)
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json={response_entity_json}")
        logger.debug("-test_response_entity_success()")
        print()

    def test_response_entity_error(self):
        """Tests an ResponseEntity object"""
        logger.debug("\n+test_response_entity_error()")
        error_entity = ErrorModel.buildError(http_status=HTTPStatus.BAD_REQUEST, message="Error")
        response = ResponseModel.buildResponse(HTTPStatus.BAD_REQUEST, error_entity)
        logger.debug(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)

        # build json response
        response_entity_json = ResponseModel.jsonResponse(HTTPStatus.BAD_REQUEST, error_entity)
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json: {response_entity_json}")
        logger.debug("-test_response_entity_error()")
        print()

    def test_build_response_with_critical(self):
        """Tests an ResponseEntity.build_response() object"""
        logger.debug("+test_build_response_with_critical()")

        try:
            named_entity = NamedModel(id=1600, name="R. Lakra")
            raise ValueError("The name should be unique!")
        except ValueError as ex:
            response = ResponseModel.buildResponse(HTTPStatus.INTERNAL_SERVER_ERROR, named_entity, exception=ex,
                                                   is_critical=True)

        logger.debug(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR.status_code, response.status)
        self.assertIsNone(response.data)
        self.assertTrue(response.hasError())
        self.assertIsNotNone(response.errors)
        self.assertTrue(len(response.errors) > 0)
        logger.debug(f"response.errors => {response.errors}")
        self.assertEqual("The name should be unique!", response.errors[0].message)

        # build json response
        response_entity_json = response.to_json()
        self.assertIsNotNone(response_entity_json)
        logger.debug(f"response_entity_json: {response_entity_json}")
        logger.debug("-test_build_response_with_critical()")
        print()
