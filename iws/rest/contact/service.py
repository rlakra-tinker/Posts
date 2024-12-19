#
# Author: Rohtash Lakra
#
from typing import Dict, Set, List
from framework.service import AbstractService
from rest.contact.models import Contact
from framework.model import ErrorModel
from framework.http import HTTPStatus


class ContactService(AbstractService):

    def __init__(self):
        self.contacts: Dict[int, Contact] = {}

    def find_by_id(self):
        """
        Returns the next ID of the account
        """
        last_id = super(ContactService, self).find_by_id()
        if not self.contacts and len(self.contacts) > 0:
            last_id = max(contact["id"] for contact in self.contacts)

        return last_id + 1

    def validate(self, contact):
        errors = []
        if contact:
            if not contact.first_name:
                errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'first_name is required!'))
            if not contact.last_name:
                errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'last_name is required!'))
            if not contact.country:
                errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'country is required!'))
            if not contact.subject:
                errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'subject is required!'))
        else:
            errors.append(ErrorModel.buildError(HTTPStatus.INVALID_DATA, 'Contact is required!'))

        return errors

    def create(self, contact: Contact) -> Contact:
        print(f"contact: {contact}")
        if not contact.id:
            contact.id = self.find_by_id()

        print(f"contact.id: {contact.id}")
        self.contacts[contact.id] = contact
        return self.contacts[contact.id]

