#
# Author: Rohtash Lakra
#
import sqlite3
from flask import g, current_app


class SQLite3Database(object):

    def __init__(self):
        self.app = None
        self.pool = None
        self.pool_name = 'sqlite3_pool'
        self.db_name = None
        self.db_user_name = None
        self.db_password = None

    def init(self, app):
        self.app = app
        self.db_name = current_app.config['posts']
        # self.create_pool()
        self.init_db()

    def create_pool(self):
        pass

    def get_connection(self):
        return self.connection

    def init_db(self):
        """Initializes the database"""
        self.connection = SQLite3Database.open_connection()
        with current_app.open_resource('data/schema.sql') as schema_file:
            self.get_connection().executescript(schema_file.read().decode('utf8'))

    def open_connection(self):
        """Opens the database connection"""
        if 'connection' not in g:
            g.connection = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
            g.connection.row_factory = sqlite3.Row

        return g.connection

    def close_connection(self, connection=None):
        """Closes the database connection"""
        connection = g.pop('connection', None)
        if connection is not None:
            connection.close()
