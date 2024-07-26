#
# Author: Rohtash Lakra
#
from werkzeug.security import generate_password_hash, gen_salt
from framework.db.sqlite import SQLite3Database
from framework.repository import AbstractRepository


class AccountRepository(AbstractRepository):

    def __init__(self):
        self.db = None
        # self.db = SQLite3Database()

    def register(self, username, password):
        register_query = '''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        '''

        # try:
        #     self.db.execute(register_query, (username, generate_password_hash(password)), )
        #     self.db.commit()
        # except self.db.IntegrityError:
        #     error = f"User {username} is already registered."
        # # else:
        # #     return redirect(url_for("auth.login"))
        return {
            "user_name": "user_name"
        }

    def find_by_id(self, user_id):
        find_query = '''
        SELECT * FROM users
        WHERE id = ?
        '''
        # return self.db.execute(find_query, (user_id,)).fetchone()

        return None
