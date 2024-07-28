#
# Author: Rohtash Lakra
#

from framework.entity.abstract import AbstractEntity


class User(AbstractEntity):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, user_name, password=None, email=None, first_name=None, last_name=None, is_admin=False):
        super().__init__(self)
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.admin = is_admin

    def __repr__(self) -> str:
        return f"{type(self).__name__} <id={self.id}, user_name={self.user_name}, email={self.email}, admin={self.admin}>"

    def json(self):
        return self.model_dump()
