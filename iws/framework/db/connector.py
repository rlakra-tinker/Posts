#
# Author: Rohtash Lakra
#
import sqlite3
from pathlib import Path

import click
from flask import Flask, g, current_app
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from common.config import Config
from framework.orm.sqlalchemy.entity import AbstractEntity
from framework.enums import KeyEnum


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

# Define Constants
KEY_CONNECTION = 'connection'
KEY_POOL_NAME = 'sqlite3_pool'
SQLITE_PREFIX = 'sqlite:///'


class DatabaseConnector(object):
    """Database Connector"""

    def __init__(self):
        current_app.logger.debug("Initializing Connector ...")
        self.UTF_8 = 'UTF-8'

    def init(self, app: Flask = None):
        current_app.logger.debug("Initializing Connector with application ...")

    def init_db(self, configs: dict = None):
        current_app.logger.debug("Initializing database ...")


class SQLite3Connector(DatabaseConnector):
    """SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured,
    SQL database engine. SQLite is the most used database engine in the world.
    """

    def __init__(self):
        """Initialize"""
        # current_app.logger.debug("Initializing SQLite3 Connector ...")
        self.app = None
        self.pool = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None
        self.db_uri = None
        self.engine = None
        self.metadata = None
        self.session = None

        # paths
        self.cur_dir = Path(__file__).parent
        # current_app.logger.debug(f"cur_dir:{self.cur_dir}")
        self.data_path = self.cur_dir.joinpath("data")
        # current_app.logger.debug(f"data_path:{self.data_path}")

    def get_connection(self):
        """Get Connection"""
        current_app.logger.debug(f"get_connection(), db_name: {self.db_name}, db_password: {self.db_password}")
        return sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def init(self, app):
        """Initialize App Context"""
        self.app = app
        with self.app.app_context():
            current_app.logger.debug(f"Initializing App Context for {app} ...")
        self._init_configs()
        # 'app.teardown_appcontext()' tells Flask to call that function when cleaning up after returning the response.
        # self.app.teardown_appcontext(self.close_connection())

        # self.create_pool()
        # app.cli.add_command() adds a new command that can be called with the flask command.
        # self.app.cli.add_command(self.init_db)

    def _init_configs(self):
        """Initializes Configs"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing Configs ...")
            #  current_app.logger.debug(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            if not self.db_name:
                self.db_name = Config.DB_NAME
                if not self.db_name.endswith(".db"):
                    self.db_name = self.db_name + '.db'

                self.db_uri = ''.join([SQLITE_PREFIX, self.db_name])
                self.db_password = Config.DB_PASSWORD
            current_app.logger.debug(f"db_name:{self.db_name}, db_password:{self.db_password}, db_uri: {self.db_uri}")

    def init_db(self, configs: dict = None):
        """Initializes the database"""
        with self.app.app_context():
            current_app.logger.debug(f"Initializing Database. configs={configs}")
            dbType = configs.get(KeyEnum.DB_TYPE)
            if dbType and dbType == KeyEnum.SQLALCHEMY:
                """Initializes the SQLAlchemy database"""
                # Set up the SQLAlchemy Database to be a local file 'posts.db'
                self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
                # SQLAlchemy DB Creation
                # The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
                self.engine = create_engine(self.db_uri, echo=True)
                self.session = Session()
                # Using our table metadata and our engine, we can generate our schema at once in our target SQLite
                # database, using a method called 'MetaData.create_all()':
                self.metadata = MetaData()
                # self.metadata.create_all(self.engine)
                AbstractEntity.metadata.create_all(self.engine)
            else:
                """Initializes the SQLite Database"""
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

    def save_entity(self, entity):
        current_app.logger.info(f"save_entity => entity={entity}")
        with Session(self.engine) as session:
            # add entity
            session.add_all([entity])
            session.commit()
            current_app.logger.info(f"Entity saved successfully!")

    def select_entity(self, entity: AbstractEntity):
        current_app.logger.info(f"select_entity => entity={entity}")
        return self.session.query(entity).first()
