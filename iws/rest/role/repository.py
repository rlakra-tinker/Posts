#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from flask import current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.repository import AbstractRepository
from framework.utils import Utils
from rest.role.schema import RoleSchema

logger = logging.getLogger(__name__)


class RoleRepository(AbstractRepository):

    def __init__(self, engine):
        super().__init__(engine)

    def create(self, role: RoleSchema) -> RoleSchema:
        """Inserts a new role"""
        current_app.logger.info(f"+create({role})")
        query = """
        INSERT INTO roles (name, active, created_at, updated_at) VALUES (?,?, ?, ?)
        """

        try:
            # current_app.logger.debug(f"query: {query}, query_values: {values}")
            cursor = self.execute(query, (role.name, role.active, role.created_at, role.updated_at))
            current_app.logger.debug(f"cursor: {cursor}, {cursor.rowcount}")
            if cursor.rowcount > 0:
                saved = self.find_by_name(role.name)
                current_app.logger.error(f"saved: {saved}")
                result = saved
        except Exception as ex:
            current_app.logger.error(f"Error={ex}, stack_trace={Utils.stack_trace(ex)}")
            print(f"Role [{role.name}] already exists!")

        current_app.logger.info(f"-create(), result: {result}")
        return result

    def find_all(self) -> List[Optional[RoleSchema]]:
        return self.execute('SELECT * FROM roles').fetchall()

    def filter(self, filters, connector='AND', operators={}) -> List[Optional[RoleSchema]]:
        current_app.logger.info(f"filter({filters}, {connector}, {operators})")
        where_clause, enumerated_filters = super().build_filters(filters, connector, operators, return_tuple=True)
        select_query = f'SELECT * FROM roles {where_clause} ORDER BY id'
        return self.execute(select_query).fetchall()

    def find_by_id(self, id) -> RoleSchema:
        return self.execute('SELECT * FROM roles WHERE id = ?', (id,)).fetchone()

    def exists(self, id: int) -> bool:
        current_app.logger.info(f"+exists({id})")
        role = self.find_by_id(id)
        current_app.logger.info(f"-exists(), role: {role}")
        return True if role else False

    def find_by_name(self, name) -> RoleSchema:
        current_app.logger.debug(f"+find_by_name({name})")
        cursor = super().execute('SELECT * FROM roles WHERE name = ?', params=(name,))
        current_app.logger.debug(f"cursor: {cursor}, {cursor.rowcount}")
        result = cursor.fetchone()
        current_app.logger.info(f"-find_by_name(), result: {result}")

    #     >>> stmt = select(User).where(User.name == "spongebob")
    # >>> with Session(engine) as session:
    # ...     for row in session.execute(stmt):
    # ...         print(row)

    # session.query(func.count(distinct(User.name)))

    def findAll(self, filters: Dict[str, Any]) -> List[Optional[RoleSchema]]:
        logger.debug(f"+findAll({filters})")
        results = List[Optional[RoleSchema]]
        with Session(self.get_engine()) as session:
            try:
                if filters:
                    # if filters.get('name'):
                    # results = session.query(RoleSchema).filter(RoleSchema.name == filters.get('name')).all()
                    results = session.query(RoleSchema).filter_by(**filters).all()
                else:
                    results = session.query(RoleSchema).all()

                # results = [row._asdict() for row in rows]
                logger.debug(f"Loaded [{len(results)}] rows => results={results}")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading records! Error={ex}")
                # session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading records! Error={ex}")
                # session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading records! Error={ex}")
                # session.rollback()
                raise ex

        logger.info(f"-findAll(), results={results}")
        return results

    def findByName(self, name: str) -> RoleSchema:
        logger.debug(f"+findByName({name})")
        results = List[Optional[RoleSchema]]
        with Session(self.get_engine()) as session:
            try:
                results = session.query(RoleSchema).filter(RoleSchema.name == name).all()
                logger.debug(f"Loaded [{len(results)}] rows => results={results}")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading records! Error={ex}")
                # session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading records! Error={ex}")
                # session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading records! Error={ex}")
                # session.rollback()
                raise ex

        logger.info(f"-findByName(), results={results}")
        return results

    def update(self, role: RoleSchema) -> RoleSchema:
        if not role or not role.id:
            raise ValueError('The Role should have an ID!')

    def delete(self, id: int):
        pass
