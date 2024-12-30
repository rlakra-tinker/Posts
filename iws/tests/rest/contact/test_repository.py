import logging
import unittest

from rest.contact.repository import ContactRepository
from rest.contact.schema import ContactSchema

logger = logging.getLogger(__name__)


class ContactRepositoryTest(unittest.TestCase):
    """Unit-tests for Repository classes"""

    def test_contact_repository(self):
        logger.debug("+test_contact_repository()")
        expected = "<class 'rest.contact.repository.ContactRepository'>"
        self.assertEqual(expected, str(ContactRepository))

        # repository object

        repository = ContactRepository()
        logger.debug(f"repository={repository}")
        self.assertIsNotNone(repository)
        expected = 'ContactRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())

        #
        contactSchema = ContactSchema(first_name="Roh", last_name="Lak", country="India",
                                      subject="Testing Contact's Schema")
        logger.debug(f"contactSchema={contactSchema}")
        contactSchema = repository.save(contactSchema)
        logger.debug(f"contactSchema={contactSchema}")
        self.assertIsNotNone(contactSchema.id)
        logger.debug("-test_contact_repository()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
