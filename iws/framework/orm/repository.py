#
# Author: Rohtash Lakra
#
import logging
from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):

    def __init__(self, engine):
        super().__init__()
        self.__engine = engine

    def __str__(self):
        """Returns the string representation of this object."""
        return f"{self.__class__.__name__} <engine={self.get_engine()}>"

    def __repr__(self):
        """Returns the string representation of this object."""
        return str(self)

    def get_engine(self):
        return self.__engine

    @abstractmethod
    def save(self, instance):
        """Saves the instance using context manager"""
        logger.debug(f"+save(), instance={instance}")
        with Session(self.__engine) as session:
            session.begin()
            try:
                session.add(instance)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug("Persisted a instance successfully!")

        logger.debug(f"-save()")

    @abstractmethod
    def save_all(self, instances: Iterable[object]):
        """Saves the instances using context manager"""
        logger.debug(f"+save_all(), instances={instances}")
        with Session(self.__engine) as session:
            session.begin()
            try:
                session.add_all(instances)
            except Exception as ex:
                logger.error(f"Failed transaction with error:{ex}")
                session.rollback()
                raise ex
            else:
                session.commit()
                logger.debug(f"Persisted [{len(instances)}] instances successfully!")
        logger.debug(f"-save_all()")
