#
# Author: Rohtash Lakra
#
import sqlite3
from flask import g, current_app
import click
from pathlib import Path
from common.config import Config
from flask_sqlalchemy import SQLAlchemy


# 'click.command()' defines a command line command called init-db that calls the 'init_db' function and shows a success
# message to the user. You can read Command Line Interface to learn more about writing commands.
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('Initializing the database ...')
    db = SQLite3Connector()
    db.init(None)
    # db.init_db()
    click.echo('Database is successfully initialized.')


# def init_app(app):
#     # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
#     app.teardown_appcontext(SQLite3Database().close_connection())
#     # app.cli.add_command() adds a new command that can be called with the flask command.
#     app.cli.add_command(init_db_command)


class DatabaseConnector(object):

    def __init__(self):
        current_app.logger.debug("Initializing Connector ...")
        self.UTF_8 = 'UTF-8'

    def init(self, app=None):
        current_app.logger.debug("Initializing Connector with application ...")

    def init_db(self):
        current_app.logger.debug("Initializing database ...")


class SQLite3Connector(DatabaseConnector):
    # Define Constants
    __CONNECTION_KEY = 'connection'
    __POOL_NAME = 'sqlite3_pool'

    def __init__(self):
        # current_app.logger.debug("Initializing SQLite3 Connector ...")
        self.app = None
        self.pool = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None
        self.db_uri = None
        self.sqlAlchemy = None

        # paths
        self.cur_dir = Path(__file__).parent
        # current_app.logger.debug(f"cur_dir:{self.cur_dir}")
        self.data_path = self.cur_dir.joinpath("data")
        # current_app.logger.debug(f"data_path:{self.data_path}")

    def get_connection(self):
        current_app.logger.debug(f"get_connection(), db_name: {self.db_name}, db_password: {self.db_password}")
        return sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def init(self, app):
        self.app = app
        with self.app.app_context():
            current_app.logger.debug(f"Initializing SQLite3 Connector for {app} ...")
        # 'app.teardown_appcontext()' tells Flask to call that function when cleaning up after returning the response.
        # self.app.teardown_appcontext(self.close_connection())

        # self.create_pool()
        # app.cli.add_command() adds a new command that can be called with the flask command.
        # self.app.cli.add_command(self.init_db)

    def init_configs(self):
        """Initializes the database"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing database configurations ...")
            #  current_app.logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            if not self.db_name:
                self.db_name = Config.DB_NAME
                if not self.db_name.endswith(".db"):
                    self.db_name = self.db_name + '.db'

                self.db_uri = ''.join(['sqlite:///', self.db_name])
                self.db_password = Config.DB_PASSWORD
                current_app.logger.debug(f"db_name:{self.db_name}, db_password:{self.db_password}, db_uri: {self.db_uri}")

    def init_db(self):
        """Initializes the database"""
        with self.app.app_context():
            self.init_configs()
            current_app.logger.debug(f"Initializing database ...")
            #  current_app.logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            try:
                connection = self.open_connection()
                # read the db-schema file and prepare db
                with open(self.data_path.joinpath('schema.sql'), encoding='UTF_8') as schema_file:
                    connection.executescript(schema_file.read())

            except Exception as ex:
                current_app.logger.debug(f'Error initializing database! Error:{ex}')
            finally:
                # close the connection
                self.close_connection()

    def init_SQLAlchemy(self):
        """Initializes the database"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing SQLAlchemy ...")
            self.init_configs()
            # Set up the SQLAlchemy Database to be a local file 'desserts.db'
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
            # Initialize Database Plugin
            self.sqlAlchemy = SQLAlchemy(self.app)
            current_app.logger.debug(f"sqlAlchemy: {self.sqlAlchemy}")

    def open_connection(self):
        """Opens the database connection"""
        with self.app.app_context():
            current_app.logger.debug("Opening database connection ...")
            if not hasattr(g, 'connection'):
                current_app.logger.debug(f"db_name:{self.db_name}, db_password:{self.db_password}")
                g.connection = self.get_connection()
                current_app.logger.debug(f"g.connection: {g.connection}")
                g.connection.row_factory = sqlite3.Row
                # g.connection.cursor(dictionary=True)
                # g.connection.autocommit = False

            return g.connection

        return None

    def close_connection(self, connection=None, error=None):
        """Closes the database connection"""
        with self.app.app_context():
            if hasattr(g, 'connection'):
                try:
                    try:
                        if error:
                            g.connection.rollback()
                            current_app.logger.debug('Rollback occurred due to an error!')

                        # closing the cursor
                        # g.cursor.close()
                    except Exception as ex:
                        current_app.logger.debug(f'Error while rollback/closing the cursor! Error:{ex}')
                    finally:
                        g.connection.close()
                except Exception as ex:
                    current_app.logger.debug(f'Error while closing the connection! Error:{ex}')
            else:
                current_app.logger.debug('No active connection!')
