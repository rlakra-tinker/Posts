import unittest

from framework.orm.repository import AbstractRepository
from framework.orm.sqlalchemy.repository import SqlAlchemyRepository


class RepositoryTest(unittest.TestCase):
    """Unit-tests for Repository classes"""

    def test_repository(self):
        print("test_repository")
        expected = "<class 'framework.orm.repository.AbstractRepository'>"
        self.assertEqual(expected, str(AbstractRepository))
        print()

    def test_sqlalchemy_repository(self):
        print("test_sqlalchemy_repository")
        expected = "<class 'framework.orm.sqlalchemy.repository.SqlAlchemyRepository'>"
        self.assertEqual(expected, str(SqlAlchemyRepository))
        # repository object
        repository = SqlAlchemyRepository(SqlAlchemyRepository.create_engine(True))
        self.assertIsNotNone(repository)
        print(repository)
        expected = 'SqlAlchemyRepository <engine=Engine(sqlite://)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())
        result = repository.save_entities(None)
        self.assertIsNone(result)
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
