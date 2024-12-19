#
# Author: Rohtash Lakra
#
import json

from framework.repository import AbstractRepository
from rest.account.model import User


class UserRepository(AbstractRepository):

    def __init__(self):
        pass

    def find_by_id(self, id: int):
        return self.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    def create(self, account: User):
        create_query = '''
        INSERT INTO users (role_id, user_name, email, first_name, last_name, password, is_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        try:
            values = (
                account.role_id, account.user_name, account.email, account.first_name, account.last_name,
                account.password,
                account.is_admin)
            self.execute(create_query, values)
        except Exception as ex:
            print(ex)

        return {
            "user_name": "user_name"
        }

    def update(id, account_json):
        if len(account_json) == 0:
            return None

        for field in [key for key in account_json.keys() if type(account_json[key]) == dict]:
            account_json[field] = json.dumps(account_json[field])

        update_query = ''

        return super().execute(update_query, {'id': id, **account_json})
