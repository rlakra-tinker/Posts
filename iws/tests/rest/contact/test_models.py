#
# Author: Rohtash Lakra
#
from tests.framework.utils import AbstractTestCase
from framework.http import HTTPStatus
from framework.model.abstract import AbstractModel, ResponseEntity, ErrorEntity
from rest.contact.models import Contact


class ModelsTest(AbstractTestCase):

    def new_contact(self, id, first_name=None, last_name=None, country=None, subject=None):
        return Contact(id=id, first_name=first_name, last_name=last_name, country=country, subject=subject)

    def test_contact(self):
        """Tests the Models object"""
        print("+test_contact()")
        contact = self.new_contact(id=16, first_name="Roh", last_name="Lakra", country="country", subject="subject")
        print(f"contact: {contact}")
        # valid object and expected results
        self.assertTrue(isinstance(contact, AbstractModel))
        self.assertFalse(isinstance(contact, AbstractTestCase))
        self.assertTrue(issubclass(Contact, object))
        self.assertFalse(issubclass(object, Contact))
        # build json response
        contact_json = contact.to_json()
        self.assertIsNotNone(contact_json)
        print(f"contact_json: {contact_json}")
        print("-test_contact()")
        print()

    def test_create_contact(self):
        """Tests an AbstractEntity object"""
        print("+test_create_contact()")
        contact = self.new_contact(id=16, first_name="Roh", last_name="Lakra", country="country", subject="subject")
        print(f"contact: {contact}")
        # valid object and expected results
        self.assertTrue(isinstance(contact, AbstractModel))
        self.assertFalse(isinstance(contact, AbstractTestCase))
        self.assertTrue(issubclass(Contact, object))
        self.assertFalse(issubclass(object, Contact))
        # build json response
        contact_json = contact.to_json()
        self.assertIsNotNone(contact_json)
        print(f"contact_json: {contact_json}")
        print("-test_create_contact()")
        print()

    def test_contact_success(self):
        """Tests an ResponseEntity object"""
        print("\n+test_contact_success()")
        contact = self.new_contact(id=16, first_name="Roh", last_name="Lakra", country="USA", subject="Test Success")
        response = ResponseEntity.response(HTTPStatus.CREATED, contact)
        print(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.CREATED.status_code, response.status)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.errors)
        self.assertFalse(response.has_error())

        # build json response
        response_json = ResponseEntity.build_response(HTTPStatus.CREATED, contact)
        self.assertIsNotNone(response_json)
        print(f"response_json: {response_json}")
        print("-test_contact_success()")
        print()

    def test_contact_error(self):
        """Tests an ResponseEntity object"""
        print("\n+test_contact_error()")
        contact = self.new_contact(id=16, first_name="Roh", last_name="Lakra", country="USA", subject="Failure")
        response = ResponseEntity.response(HTTPStatus.BAD_REQUEST, contact, message="Test Failure")
        print(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, response.status)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.has_error())
        self.assertIsNotNone(response.errors)

        # build json response
        response_json = ResponseEntity.build_response(HTTPStatus.BAD_REQUEST, contact)
        self.assertIsNotNone(response_json)
        print(f"response_json: {response_json}")
        print("-test_contact_error()")
        print()


    def test_response(self):
        """Tests an ResponseEntity object"""
        print("\n+test_response()")
        ResponseEntity
        contact = self.new_contact(id=16, first_name="Roh", last_name="Lakra", country="USA", subject="Failure")
        errors = [ErrorEntity.error(HTTPStatus.INVALID_DATA, message='First name should provide!'),
                  ErrorEntity.error(HTTPStatus.INVALID_DATA, message='Last name should provide!')]
        response = ResponseEntity(status=HTTPStatus.BAD_REQUEST.status_code, data=contact, errors=errors)
        print(f"response: {response}")
        self.assertIsNotNone(response)
        self.assertEqual(HTTPStatus.BAD_REQUEST.status_code, response.status)
        self.assertIsNotNone(response.data)
        self.assertTrue(response.has_error())
        self.assertIsNotNone(response.errors)

        # build json response
        response_json = response.to_json()
        self.assertIsNotNone(response_json)
        print(f"response_json: {response_json}")
        print("-test_response()")
        print()
