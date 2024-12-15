#
# Author: Rohtash Lakra
#

from framework.model.abstract import AbstractModel


class Role(AbstractModel):
    name: str = None
    active: bool = None

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, name={self.name}, active={self.active}, created_at={self.get_created_at()}, updated_at={self.get_updated_at()}>"

    def json(self):
        return self.model_dump()

    @staticmethod
    def create(name, active):
        """Creates the contact object with values"""
        # print(f"name:{name}, active:{active}")
        return Role(name=name, active=active)
