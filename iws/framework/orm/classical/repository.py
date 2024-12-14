#
# Author: Rohtash Lakra
#
from abc import ABC

from framework.orm.repository import AbstractRepository


class ClassicalRepository(AbstractRepository, ABC):

    def __init__(self, engine):
        super().__init__(engine)
