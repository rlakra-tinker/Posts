#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import Blueprint, render_template, make_response, request, redirect, url_for
from iws.framework.http import HTTPStatus
from iws.framework.entity.abstract import ErrorEntity

#
bp = Blueprint("admin", __name__, url_prefix="/admin")
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

# holds accounts in memory
accounts = []


# Returns the next ID of the account
def _find_next_id():
    last_id = 0
    if not accounts and len(accounts) > 0:
        last_id = max(account["id"] for account in accounts)

    return last_id + 1


# register a new account
@bp.route("/")
def index():
    """
    register a new account
    """
    return render_template("admin/index.html")


# register a new account
@bp.get("/register")
def register():
    """
    register a new account
    """
    return render_template("admin/register.html")


@bp.post("/register")
def post_register():
    print(request)
    if request.is_json:
        user = request.get_json()
        user["id"] = _find_next_id()
        accounts.append(user)
        return user, 201

    return make_response(ErrorEntity(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Invalid JSON object!"))


# login to an account
@bp.get("/login")
def login():
    """
    login to an account
    """
    return render_template("admin/login.html")


@bp.post("/login")
def post_login():
    print(request)
    if request.is_json:
        user = request.get_json()
        print(f"user:{user}")
        if not accounts:
            for account in accounts:
                if account['user_name'] == user.user_name:
                    return make_response(HTTPStatus.OK, account)

    response = ErrorEntity.get_error(HTTPStatus.NOT_FOUND, "Account is not registered!")
    print(response)

    return make_response(response)


# view profile
@bp.get("/profile")
def profile():
    """
    view profile
    """
    return render_template("admin/profile.html")


# forgot-password
@bp.get("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    return render_template("admin/forgot-password.html")


# Logout Page
@bp.post("/logout")
def logout():
    """
    About Us Page
    """
    # return render_template("index.html")
    return redirect(url_for('iws.webapp.index'))

