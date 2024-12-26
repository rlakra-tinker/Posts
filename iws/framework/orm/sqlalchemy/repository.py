#
# Author: Rohtash Lakra
#
import json
import logging
from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any
from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm.mapper import Mapper

from framework.orm.repository import AbstractRepository
from framework.orm.sqlalchemy.schema import BaseSchema

logger = logging.getLogger(__name__)


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, engine):
        super().__init__(engine)

    @abstractmethod
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[BaseSchema]]:
        pass

    def save(self, instance: BaseSchema) -> BaseSchema:
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
                    # Refresh to get any other DB-generated values
                    session.refresh(instance)
        else:
            logger.warning(f"No instance provided to persist!")

        logger.debug(f"-save(), instance={instance}")
        return instance

    def save_all(self, instances: Iterable[BaseSchema]):
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

    def findById(self, instance: BaseSchema) -> Optional[List[dict]]:
        """Finds the record by id in the provided table and parses as list of dict.

        :param Engine engine: Database engine to handle raw SQL queries.
        :param str table: table name which records to fetch.

        :return: Optional[List[dict]]
        """
        logger.debug(f"+findById({instance})")
        results = dict()
        with Session(self.get_engine()) as session:
            try:
                # session.begin()
                rows = session.query(instance).filter(instance.id == id()).one()
                # rows = session.execute(text(query)).fetchall()
                results = [row._asdict() for row in rows]
                logger.debug(f"Loaded [{rows.rowcount}] rows => results={results}")
                logger.debug(f"Loaded [{rows.rowcount}] rows => results={json.dumps(results, indent=2)}")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading records! Error={ex}")
                # session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading records! Error={ex}")
                # session.rollback()
                raise ex
        logger.debug(f"-findById(), results={results}")

    def findAll(self, table: str, fields=[]) -> Optional[List[dict]]:
        """Finds rows of the provided table from the database and parses as list of dict.

        :param Engine engine: Database engine to handle raw SQL queries.
        :param str table: table name which records to fetch.

        :return: Optional[List[dict]]
        """
        logger.debug(f"+findAll({table}, {fields})")
        results = dict()
        try:
            query = f'SELECT {fields} FROM {table}'
            with Session(self.get_engine()) as session:
                rows = session.execute(text(query), ).fetchall()
                results = [row._asdict() for row in rows]
                logger.debug(f"Loaded [{rows.rowcount}] rows => results={results}")
                logger.debug(f"Loaded [{rows.rowcount}] rows => results={json.dumps(results, indent=2)}")
        except SQLAlchemyError as ex:
            logger.error(f"SQLAlchemyError while loading records! Error={ex}")
        except Exception as ex:
            logger.error(f"Exception while loading records! Error={ex}")

        logger.debug(f"-findAll(), results={results}")

    def updateObjects(self, table: str, update_json=[]) -> Optional[List[dict]]:
        """Finds rows of the provided table from the database and parses as list of dict.

        :param Engine engine: Database engine to handle raw SQL queries.
        :param str table: table name which records to fetch.

        :return: Optional[List[dict]]
        """
        logger.debug(f"+updateObjects({table}, {update_json})")
        query = f'UPDATE {table} {self.build_update_set_fields(update_json)}'
        with Session(self.get_engine()) as session:
            try:
                rows = session.execute(text(query), ).fetchall()
                logger.debug(f"Updated [{rows.rowcount}] rows => {rows}")
                return rows
            except SQLAlchemyError as ex:
                logger.error(f"SQLAlchemyError while updating records! Error={ex}")
                session.rollback()
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
            else:
                session.commit()

    def update(self, mapper: Mapper[BaseSchema], mappings: List[BaseSchema]) -> List[Optional[BaseSchema]]:
        """Updates an instance into database via the ORM flush process."""
        logger.debug(f"+update(), mapper={mapper}, mappings={mappings}")
        if mappings is not None:
            with Session(self.get_engine()) as session:
                try:
                    session.bulk_update_mappings(mapper, mappings)
                    session.flush()
                    session.commit()
                    logger.debug(f"Persisted a instance successfully!")
                except Exception as ex:
                    logger.error(f"Failed transaction with error:{ex}")
                    session.rollback()
                else:
                    # Refresh to get any other DB-generated values
                    session.refresh(mappings)
        else:
            logger.warning(f"No instance provided to update!")

        logger.debug(f"-update(), mappings={mappings}")
        return mappings
