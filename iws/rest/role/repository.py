#
# Author: Rohtash Lakra
#
import logging
from abc import ABC
from typing import List, Optional, Dict, Any

from sqlalchemy import update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.repository import AbstractRepository
from rest.role.schema import RoleSchema

logger = logging.getLogger(__name__)


class RoleRepository(AbstractRepository, ABC):

    def __init__(self, engine):
        super().__init__(engine)

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[RoleSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        listOfRoles = List[Optional[RoleSchema]]
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            # session.begin()
            try:
                if filters:
                    listOfRoles = session.query(RoleSchema).filter_by(**filters).all()
                else:
                    listOfRoles = session.query(RoleSchema).all()

                logger.debug(f"Loaded [{len(listOfRoles)}] rows => listOfRoles={listOfRoles}")

                # commit.  The pending changes above
                # are flushed via flush(), the Transaction
                # is committed, the Connection object closed
                # and discarded, the underlying DBAPI connection
                # returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading records! Error={ex}")
                session.rollback()
                raise ex
            except:
                # on rollback, the same closure of state
                # as that of commit proceeds.
                session.rollback()
                raise
            finally:
                # close the Session.  This will expunge any remaining
                # objects as well as reset any existing SessionTransaction
                # state.  Neither of these steps are usually essential.
                # However, if the commit() or rollback() itself experienced
                # an unanticipated internal failure (such as due to a mis-behaved
                # user-defined event handler), .close() will ensure that
                # invalid state is removed.
                session.close()

        logger.debug(f"-findByFilter(), listOfRoles={listOfRoles}")
        return listOfRoles

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

    def update(self, roleSchema: RoleSchema) -> RoleSchema:
        logger.debug(f"+update({roleSchema})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                results = session.execute(
                    update(RoleSchema)
                    .values(roleSchema.to_json())
                    .where(RoleSchema.id == roleSchema.id)
                ).rowcount
                logger.debug(f"Updated [{results}] rows.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        with Session(self.get_engine()) as session:
            try:
                listOfRoles = self.findByFilter({"id": id})
                # roles = session.query(RoleSchema).filter(RoleSchema.id == id).all()
                for roleSchema in listOfRoles:
                    logger.debug(f"Deleting role with id=[{roleSchema.id}]")
                    session.delete(roleSchema)

                # session.delete(roleSchema)
                logger.debug(f"Deleted [{len(listOfRoles)}] rows successfully.")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating records! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating records! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")
