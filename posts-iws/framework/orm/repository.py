#
# Author: Rohtash Lakra
#
import abc
from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    def __init__(self, engine):
        super().__init__()
        self.__engine = engine

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} <engine={self.get_engine()}>"

    def __str__(self):
        return self.__repr__()

    def get_engine(self):
        return self.__engine

    @abstractmethod
    def save_entities(self, entities: list = None):
        print(f'save_entities({entities})')
        pass
