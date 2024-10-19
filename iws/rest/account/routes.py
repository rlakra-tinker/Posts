#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
from flask import Blueprint, make_response, request, session, g, redirect, url_for
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity
from rest.account.service import AccountService
from rest.account.models import Account

#
bp = Blueprint("accounts", __name__, url_prefix="/accounts")
"""
Making a Flask Blueprint:

Create an instance of it named 'bp'.

Note that in the below code, some arguments are specified when creating the Blueprint object.
The first argument, 'api', is the Blueprint’s name, which is used by Flask’s routing mechanism (and identifies it in your Flask project). 
The second argument, '__name__', is the Blueprint’s import name, which Flask uses to locate the Blueprint’s resources.
The third argument, 'url_prefix="/api"', the path to prepend to all of the Blueprint’s URLs.

There are other optional arguments that you can provide to alter the Blueprint’s behavior:

static_folder: the folder where the Blueprint’s static files can be found
static_url_path: the URL to serve static files from
template_folder: the folder containing the Blueprint’s templates
url_prefix: the path to prepend to all of the Blueprint’s URLs
subdomain: the subdomain that this Blueprint’s routes will match on by default
url_defaults: a dictionary of default values that this Blueprint’s views will receive
root_path: the Blueprint’s root directory path, whose default value is obtained from the Blueprint’s import name

Note that all paths, except root_path, are relative to the Blueprint’s directory.

However, a Flask Blueprint is not actually an application. It needs to be registered in an application before you can run it. 
When you register a Flask Blueprint in an application, you’re actually extending the application with the contents of the Blueprint.
This is the key concept behind any Flask Blueprint. They record operations to be executed later when you register them on an application.

The Blueprint object 'bp' has methods and decorators that allow you to record operations to be executed when registering 
the Flask Blueprint in an application to extend it.

Here are the Blueprint objects most used decorators that you may find useful:

- '.route()' to associate a view function to a URL route
- '.errorhandler()' to register an error handler function
- '.before_request()' to execute an action before every request
- '.after_request()' to execute an action after every request
- '.app_template_filter()' to register a template filter at the application level

When you register the Flask Blueprint in an application, you extend the application with its contents.

"""

# account's service
accountService = AccountService()


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # g.user = accountService.find_by_id(user_id)
        g.user = None


@bp.post("/register/")
def register():
    print(request)
    if request.is_json:
        user = accountService.register()
        user = Account.model_construct(request.get_json())
        accountService.add(user)
        return user, 201
    else:
        username = request.form['username']
        password = request.form['password']
        user = accountService.register(username, password)

        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        response = None
        if error is None:
            try:
                response = accountService.register()
            except Exception as ex:
                error = f"User '{username}' is already registered! ex:{ex}"
            else:
                return redirect(url_for("iws.api.login"))

        # flash(error)

        if response:
            return response

    return make_response(ErrorEntity(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Invalid JSON object!"))


@bp.post("/login")
def login():
    print(request)
    if request.is_json:
        user = request.get_json()
        print(f"user:{user}")
        # if not accounts:
        #     for account in accounts:
        #         if account['user_name'] == user.user_name:
        #             return make_response(HTTPStatus.OK, account)

    response = ErrorEntity.error(HTTPStatus.NOT_FOUND, "Account is not registered!")
    print(response)

    return make_response(response)


# Logout Page
@bp.post("/logout")
def logout():
    """
    logout
    """
    session.clear()


@bp.post("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    pass
