#
# Author: Rohtash Lakra
#
from typing import Dict
from framework.service import AbstractService
from .models import Contact


class ContactService(AbstractService):

    def __init__(self):
        self.contacts: Dict[int, Contact] = {}

    def _find_next_id(self):
        """
        Returns the next ID of the account
        """
        last_id = super(ContactService, self)._find_next_id()
        if not self.contacts and len(self.contacts) > 0:
            last_id = max(contact["id"] for contact in self.contacts)

        return last_id + 1

    def validate(self, contact):
        print(f"contact={contact.to_json()}")
        if not contact:
            return 'contact is required.'
        elif not contact.first_name:
            return 'first_name is required.'
        elif not contact.last_name:
            return 'last_name is required.'
        elif not contact.country:
            return 'country is required.'
        elif not contact.subject:
            return 'subject is required.'

        return None

    def add(self, contact: Contact):
        print(f"contact: {contact}")
        contact.id = self._find_next_id()
        print(f"contact.id: {contact.id}")
        self.contacts[contact.id] = contact

    def addContact(self, first_name, last_name, country, subject):
        contact = Contact(first_name=first_name, last_name=last_name, country=country, subject=subject)
        self.add(contact)
        return contact.json()
