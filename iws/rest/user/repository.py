#
# Author: Rohtash Lakra
#

import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import update, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

from framework.orm.sqlalchemy.repository import SqlAlchemyRepository
from globals import connector
from rest.user.schema import UserSchema, AddressSchema

logger = logging.getLogger(__name__)


class UserRepository(SqlAlchemyRepository):
    """The UserRepository handles a schema-centric database persistence for users."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[UserSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        userSchemas = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                if filters:
                    userSchemas = session.query(UserSchema).filter_by(**filters).all()
                else:
                    userSchemas = session.query(UserSchema).all()

                logger.debug(f"Loaded [{len(userSchemas)}] users => userSchemas={userSchemas}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading users! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading users! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading users! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise
            finally:
                # close the Session.
                # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                # Neither of these steps are usually essential.
                # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                # is removed.
                session.close()

        logger.debug(f"-findByFilter(), userSchemas={userSchemas}")
        return userSchemas

    def findByUsername(self, userName: str) -> UserSchema:
        logger.debug(f"+findByUsername({userName})")
        results = List[Optional[UserSchema]]
        with Session(self.get_engine()) as session:
            try:
                results = session.query(UserSchema).filter(UserSchema.name == userName).all()
                logger.debug(f"Loaded [{len(results)}] users => results={results}")
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading user by name! Error={ex}")
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading user by name! Error={ex}")
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading user by name! Error={ex}")
                raise ex

        logger.info(f"-findByUsername(), results={results}")
        return results

    def update(self, userSchema: UserSchema) -> UserSchema:
        logger.debug(f"+update({userSchema})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                userSchema.updated_at = func.now()
                results = session.execute(
                    update(UserSchema)
                    .values(userSchema.to_json())
                    .where(UserSchema.id == userSchema.id)
                ).rowcount
                logger.debug(f"Updated [{results}] user.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating user! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating user! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating user! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, filters: Dict[str, Any]) -> None:
        logger.debug(f"+delete({filters})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                userSchema = session.query(UserSchema).filter_by(**filters).one()
                logger.debug(f"Deleting userSchema={userSchema}")
                session.delete(userSchema)
                logger.debug("User is successfully deleted.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating users! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating users! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating users! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")

    def bulkDelete(self, ids: list[int]) -> None:
        logger.debug(f"+bulkDelete({ids})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                userSchemas = self.findByFilter({"id": ids})
                for userSchema in userSchemas:
                    logger.debug(f"Deleting user with id=[{userSchema.id}]")
                    session.delete(userSchema)

                logger.debug(f"Deleted [{len(userSchemas)}] users successfully.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while bulk deleting users! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while bulk deleting users! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while bulk deleting users! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-bulkDelete()")


class AddressRepository(SqlAlchemyRepository):
    """The AddressRepository handles a schema-centric database persistence for addresses."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[AddressSchema]]:
        """Returns records by filter or empty list"""
        logger.debug(f"+findByFilter({filters})")
        addressSchemas = None
        # verbose version of what a context manager will do
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                if filters:
                    addressSchemas = session.query(AddressSchema).filter_by(**filters).all()
                else:
                    addressSchemas = session.query(AddressSchema).all()

                logger.debug(f"Loaded [{len(addressSchemas)}] addresses => addressSchemas={addressSchemas}")

                # Commit:
                # The pending changes above are flushed via flush(), the Transaction is committed, the Connection
                # object closed and discarded, the underlying DBAPI connection returned to the connection pool.
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while loading addresses! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while loading addresses! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while loading addresses! Error={ex}")
                # on rollback, the same closure of state as that of commit proceeds.
                session.rollback()
                raise ex
            except:
                # on rollback, the same closure of state as that of commit proceeds.
                logger.error(f"Exception while loading addresses!")
                session.rollback()
                raise
            finally:
                # close the Session.
                # This will expunge any remaining objects as well as reset any existing 'SessionTransaction' state.
                # Neither of these steps are usually essential.
                # However, if the commit() or rollback() itself experienced an unanticipated internal failure
                # (such as due to a mis-behaved user-defined event handler), .close() will ensure that invalid state
                # is removed.
                session.close()

        logger.debug(f"-findByFilter(), addressSchemas={addressSchemas}")
        return addressSchemas

    def update(self, addressSchema: AddressSchema) -> AddressSchema:
        logger.debug(f"+update({addressSchema})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                addressSchema.updated_at = func.now()
                results = session.execute(
                    update(AddressSchema)
                    .values(addressSchema.to_json())
                    .where(AddressSchema.id == addressSchema.id)
                ).rowcount
                logger.debug(f"Updated [{results}] addresses.")

                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while updating addresses! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while updating addresses! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating address! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-update(), results={results}")
        return results

    def delete(self, filters: Dict[str, Any]) -> None:
        logger.debug(f"+delete({filters})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                addressSchema = session.query(AddressSchema).filter_by(**filters).one()
                logger.debug(f"Deleting addressSchema={addressSchema}")
                session.delete(addressSchema)
                logger.info("Address is successfully deleted.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while deleting addresses! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while deleting addresses! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while updating deleting addresses! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-delete()")

    def bulkDelete(self, ids: list[int]) -> None:
        logger.debug(f"+bulkDelete({ids})")
        with Session(bind=self.get_engine(), expire_on_commit=False) as session:
            try:
                addressSchemas = self.findByFilter({"id": ids})
                for addressSchema in addressSchemas:
                    logger.debug(f"Deleting address with id=[{addressSchema.id}]")
                    session.delete(addressSchema)

                logger.debug(f"Deleted [{len(addressSchemas)}] addresses successfully.")
                session.commit()
            except NoResultFound as ex:
                logger.error(f"NoResultFound while bulk deleting addresses! Error={ex}")
                session.rollback()
                raise ex
            except MultipleResultsFound as ex:
                logger.error(f"MultipleResultsFound while bulk deleting addresses! Error={ex}")
                session.rollback()
                raise ex
            except Exception as ex:
                logger.error(f"Exception while deleting bulk addresses! Error={ex}")
                session.rollback()
                raise ex

        logger.info(f"-bulkDelete()")
