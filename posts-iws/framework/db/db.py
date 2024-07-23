#
# Author: Rohtash Lakra
#
from sqlite import SQLite3Database
import click


# click.command() defines a command line command called init-db that calls the init_db function and shows a success
# message to the user. You can read Command Line Interface to learn more about writing commands.
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    SQLite3Database.init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(SQLite3Database.close_db())
    # app.cli.add_command() adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)



