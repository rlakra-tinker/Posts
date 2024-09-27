#
# Author: Rohtash Lakra
#

from framework.model.abstract import AbstractEntity


class Account(AbstractEntity):
    role_id: int = None
    user_name: str = None
    email: str = None
    first_name: str = None
    last_name: str = None
    password: str = None
    is_admin: bool = False

    def json(self):
        return self.model_dump()

    def from_json(self, json_object: dict):
        return Account(role_id=json_object.get('role_id'),
                       user_name=json_object.get('user_name'),
                       email=json_object.get('email'),
                       first_name=json_object.get('first_name'),
                       last_name=json_object.get('last_name'),
                       password=json_object.get('password'),
                       is_admin=bool(json_object.get('is_admin', False)))
