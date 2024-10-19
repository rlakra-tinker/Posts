#
# Author: Rohtash Lakra
#
from iws.framework.orm.repository import AbstractRepository


class ClassicalRepository(AbstractRepository):

    def __init__(self, engine):
        super().__init__(engine)


