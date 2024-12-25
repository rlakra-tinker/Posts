import logging
import unittest

from framework.orm.repository import AbstractRepository, createEngine
from framework.orm.sqlalchemy.repository import SqlAlchemyRepository

logger = logging.getLogger(__name__)


class RepositoryTest(unittest.TestCase):
    """Unit-tests for Repository classes"""

    def test_repository(self):
        logger.debug("+test_repository()")
        expected = "<class 'framework.orm.repository.AbstractRepository'>"
        self.assertEqual(expected, str(AbstractRepository))
        logger.debug("-test_repository()")

    def test_sqlalchemy_repository(self):
        logger.debug("+test_sqlalchemy_repository()")
        expected = "<class 'framework.orm.sqlalchemy.repository.SqlAlchemyRepository'>"
        self.assertEqual(expected, str(SqlAlchemyRepository))
        # repository object
        engine = createEngine("sqlite:///testPosts.db", True)
        repository = SqlAlchemyRepository(engine)
        self.assertIsNotNone(repository)
        logger.debug(repository)
        expected = 'SqlAlchemyRepository <engine=Engine(sqlite:///testPosts.db)>'
        self.assertEqual(expected, str(repository))
        self.assertIsNotNone(repository.get_engine())
        result = repository.save_all(None)
        self.assertIsNone(result)
        logger.debug("-test_sqlalchemy_repository()")


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
