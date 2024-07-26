#
# Author: Rohtash Lakra
#

from framework.model.abstract import AbstractEntity


class User(AbstractEntity):
    user_name: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    email: str = None
    is_admin: bool = False

    def json(self):
        return self.model_dump()
