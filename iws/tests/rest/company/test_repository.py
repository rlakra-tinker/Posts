import logging
import unittest

from rest.company.repository import CompanyRepository
from rest.company.schema import CompanySchema

logger = logging.getLogger(__name__)


class UserRepositoryTest(unittest.TestCase):
    """Unit-tests for Repository classes"""

    def test_company_repository(self):
        logger.debug("+test_company_repository()")
        expected = "<class 'rest.company.repository.CompanyRepository'>"
        self.assertEqual(expected, str(CompanyRepository))

        # repository object

        repository = CompanyRepository()
        logger.debug(f"repository={repository}")
        self.assertIsNotNone(repository)
        expected = 'CompanyRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())

        #
        instance = CompanySchema(name="Lakra Inc.")

        logger.debug(f"instance={instance}")
        instance = repository.save(instance)
        logger.debug(f"instance={instance}")
        self.assertIsNotNone(instance.id)
        self.assertEqual("Lakra Inc.", instance.name)
        logger.debug("-test_company_repository()")
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
