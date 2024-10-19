#
# Author: Rohtash Lakra
#
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from framework.orm.repository import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, engine):
        super().__init__(engine)

    @staticmethod
    def create_engine(debug: bool = False):
        return create_engine("sqlite://", echo=debug)

    def save_entities(self, entities: list = None):
        """Persists the given entities into database"""
        print(f'save_entities({entities})')
        if entities is not None:
            with Session(self.get_engine()) as session:
                # persist all entities
                session.add_all(entities)
                session.commit()

