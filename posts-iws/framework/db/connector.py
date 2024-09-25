#
# Author: Rohtash Lakra
#
import sqlite3
from flask import g
import click
from pathlib import Path
from webapp.config import Config
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
        print("Initializing Connector ...")
        self.UTF_8 = 'UTF-8'

    def init(self, app=None):
        print("Initializing Connector with application ...")

    def init_db(self):
        print("Initializing database ...")


class SQLite3Connector(DatabaseConnector):
    # Define Constants
    __CONNECTION_KEY = 'connection'
    __POOL_NAME = 'sqlite3_pool'

    def __init__(self):
        print("Initializing SQLite3 Connector ...")
        self.app = None
        self.pool = None
        self.db_name: str = None
        self.db_user_name = None
        self.db_password = None
        self.db_uri = None
        self.sqlAlchemy = None

        # paths
        self.cur_dir = Path(__file__).parent
        print(f"cur_dir:{self.cur_dir}")
        self.data_path = self.cur_dir.joinpath("data")
        print(f"data_path:{self.data_path}")
        print()

    def get_connection(self):
        print(f"get_connection(), db_name: {self.db_name}, db_password: {self.db_password}")
        return sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)

    def init(self, app):
        print(f"Initializing SQLite3 Connector for {app} ...")
        self.app = app
        # 'app.teardown_appcontext()' tells Flask to call that function when cleaning up after returning the response.
        # self.app.teardown_appcontext(self.close_connection())

        # self.create_pool()
        # app.cli.add_command() adds a new command that can be called with the flask command.
        # self.app.cli.add_command(self.init_db)

    def init_configs(self):
        """Initializes the database"""
        print(f"Initializing database configurations ...")
        with self.app.app_context():
            # print(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            if not self.db_name:
                self.db_name = Config.DB_NAME
                if not self.db_name.endswith(".db"):
                    self.db_name = self.db_name + '.db'

                self.db_uri = ''.join(['sqlite:///', self.db_name])
                self.db_password = Config.DB_PASSWORD
                print(f"db_name:{self.db_name}, db_password:{self.db_password}, db_uri: {self.db_uri}")

    def init_db(self):
        """Initializes the database"""
        self.init_configs()
        print(f"Initializing database ...")
        with self.app.app_context():
            # print(f"current_app: {current_app}, current_app.config: {current_app.config}")
            # read db-name from app's config
            try:
                connection = self.open_connection()
                # read the db-schema file and prepare db
                with open(self.data_path.joinpath('schema.sql'), encoding='UTF_8') as schema_file:
                    connection.executescript(schema_file.read())

            except Exception as ex:
                print(f'Error initializing database! Error:{ex}')
            finally:
                # close the connection
                self.close_connection()


    def init_SQLAlchemy(self):
        """Initializes the database"""
        print(f"Initializing SQLAlchemy ...")
        self.init_configs()
        with self.app.app_context():
            # Set up the SQLAlchemy Database to be a local file 'desserts.db'
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
            # Initialize Database Plugin
            self.sqlAlchemy = SQLAlchemy(self.app)
            print(f"sqlAlchemy: {self.sqlAlchemy}")

    def open_connection(self):
        """Opens the database connection"""
        print("Opening database connection ...")
        with self.app.app_context():
            if not hasattr(g, 'connection'):
                print(f"db_name:{self.db_name}, db_password:{self.db_password}")
                g.connection = self.get_connection()
                print(f"g.connection: {g.connection}")
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
                            print('Rollback occurred due to an error!')

                        # closing the cursor
                        # g.cursor.close()
                    except Exception as ex:
                        print(f'Error while rollback/closing the cursor! Error:{ex}')
                    finally:
                        g.connection.close()
                except Exception as ex:
                    print(f'Error while closing the connection! Error:{ex}')
            else:
                print('No active connection!')
