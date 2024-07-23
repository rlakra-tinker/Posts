#
# Author: Rohtash Lakra
#

from framework.entity import AbstractEntity


class User(AbstractEntity):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, user_name, password=None, first_name=None, last_name=None, is_admin=False):
        super.__init__(self)
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.admin = last_name

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.id}, user_name={self.user_name}>"
