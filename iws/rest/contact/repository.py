#
# Author: Rohtash Lakra
#
# from werkzeug.security import generate_password_hash, gen_salt
# from framework.db.sqlite import SQLite3Database
from framework.orm.sqlalchemy.repository import SqlAlchemyRepository
from globals import connector


class ContactRepository(SqlAlchemyRepository):
    """The ContactRepository handles a schema-centric database persistence for contacts."""

    def __init__(self):
        super().__init__(engine=connector.engine)

    def register(self, username, password):
        """
        Registers the contact with username and password

        Parameters:
            username: unique identity of the user
            password: password for security
        """
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
