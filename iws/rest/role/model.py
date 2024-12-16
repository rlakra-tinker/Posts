#
# Author: Rohtash Lakra
#

from framework.model import AbstractModel


class Role(AbstractModel):
    name: str = None
    active: bool = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, name={self.name}, active={self.active}, {super()._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)

    def json(self):
        return self.model_dump()

    @staticmethod
    def create(name, active):
        """Creates the contact object with values"""
        # print(f"name:{name}, active:{active}")
        return Role(name=name, active=active)
