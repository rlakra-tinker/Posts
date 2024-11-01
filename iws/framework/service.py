#
# Author: Rohtash Lakra
#
from abc import abstractmethod


class AbstractService:
    """
    An abstract service for all other services inherits.
    """

    # Returns the next ID of the account
    @abstractmethod
    def find_by_id(self, id: int):
        pass


class DataStore:

    def init(self, app):
        self.app = app

    @property
    def get_app(self):
        return self.app

