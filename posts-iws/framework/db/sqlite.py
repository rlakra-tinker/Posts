#
# Author: Rohtash Lakra
#
import sqlite3
from flask import g, current_app


class SQLite3Database(object):

    def __init__(self):
        self.db = SQLite3Database.get_db()
        pass

    def getDatabase(self):
        return self.db

    @staticmethod
    def init_db():
        db = SQLite3Database.get_db()
        with current_app.open_resource('data/schema.sql') as schema_file:
            db.executescript(schema_file.read().decode('utf8'))

    @staticmethod
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db

    @staticmethod
    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()
