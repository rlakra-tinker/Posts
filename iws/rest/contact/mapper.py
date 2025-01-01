#
# Author: Rohtash Lakra
#
from framework.orm.mapper import Mapper
from rest.contact.model import Contact
from rest.contact.schema import ContactSchema


class ContactMapper(Mapper):

    @classmethod
    # @override
    def fromSchema(self, contactSchema: ContactSchema) -> Contact:
        return Contact(**contactSchema.toJSONObject())

    @classmethod
    # @override
    def fromModel(self, contact: Contact) -> ContactSchema:
        return ContactSchema(**contact.toJSONObject())
