#
# Author: Rohtash Lakra
# References:
# - https://realpython.com/flask-blueprint/
# - https://flask.palletsprojects.com/en/2.3.x/tutorial/views/#require-authentication-in-other-views
#
from rest.account.v1 import bp as bp_account_v1
from flask import make_response, request, session, g, redirect, url_for
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity
from rest.account.service import AccountService
from rest.account.models import Account


# account's service
accountService = AccountService()


@bp_account_v1.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # g.user = accountService.find_by_id(user_id)
        g.user = None


@bp_account_v1.post("/register/")
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


@bp_account_v1.post("/login")
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
@bp_account_v1.post("/logout")
def logout():
    """
    logout
    """
    session.clear()


@bp_account_v1.post("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    pass
