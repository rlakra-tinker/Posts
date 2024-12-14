#
# Author: Rohtash Lakra
#
import logging
from abc import ABC
from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from framework.orm.repository import AbstractRepository

logger = logging.getLogger(__name__)


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, engine):
        super().__init__(engine)

    @staticmethod
    def create_engine(debug: bool = False):
        return create_engine("sqlite://", echo=debug)

    def save(self, instance):
        """Persists the given entity into database"""
        logger.debug(f"+save(), instance={instance}")
        if instance is not None:
            with Session(self.get_engine()) as session:
                try:
                    session.add(instance)
                    session.commit()
                    logger.debug(f"Persisted a instance successfully!")
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
        else:
            logger.warning(f"No instance provided to persist!")
        logger.debug(f"-save()")

    def save_all(self, instances: Iterable[object]):
        """Persists the given entities into database"""
        logger.debug(f"+save_all(), instances={instances}")
        if instances is not None:
            with Session(self.get_engine()) as session:
                try:
                    session.add_all(instances)
                    session.commit()
                    logger.debug(f"Persisted [{len(instances)}] instances successfully!")
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
        else:
            logger.warning(f"No instances provided to persist!")
        logger.debug(f"-save_all()")
