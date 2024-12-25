#
# Author: Rohtash Lakra
#
import json
import logging
from abc import ABC
from typing import Dict, Any, List, Optional

from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.repository import AbstractRepository
from rest.account.schema import UserSchema

logger = logging.getLogger(__name__)


class UserRepository(AbstractRepository, ABC):

    def __init__(self, engine):
        super().__init__(engine)

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[UserSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        listOfUsers = List[Optional[UserSchema]]
        with Session(self.get_engine()) as session:
            try:
                if filters:
                    listOfUsers = session.query(UserSchema).filter_by(**filters).all()
                else:
                    listOfUsers = session.query(UserSchema).all()

                logger.debug(f"Loaded [{len(listOfUsers)}] rows => listOfUsers={listOfUsers}")
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

        logger.debug(f"-findByFilter(), listOfUsers={listOfUsers}")
        return listOfUsers

    def find_by_id(self, id: int):
        return self.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    def create(self, account: UserSchema):
        create_query = '''
        INSERT INTO users (role_id, user_name, email, first_name, last_name, password, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        try:
            values = (
                account.role_id, account.user_name, account.email, account.first_name, account.last_name,
                account.password,
                account.is_admin)
            self.execute(create_query, values)
        except Exception as ex:
            print(ex)

        return {
            "user_name": "user_name"
        }

    def update(id, account_json):
        if len(account_json) == 0:
            return None

        for field in [key for key in account_json.keys() if type(account_json[key]) == dict]:
            account_json[field] = json.dumps(account_json[field])

        update_query = ''

        return super().execute(update_query, {'id': id, **account_json})
