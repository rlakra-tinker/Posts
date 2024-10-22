#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
from flask import render_template, make_response, request, redirect, url_for
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity, ResponseEntity
from account.models import User
from account import bp

# holds accounts in memory
accounts = []


# Returns the next ID of the account
def _find_next_id():
    last_id = 0
    if not accounts and len(accounts) > 0:
        last_id = max(account["id"] for account in accounts)

    return last_id + 1


# register a new account
# @bp.route("/register", methods=[HTTPMethod.GET, HTTPMethod.POST])
@bp.get("/register")
def register_view():
    """
    register a new account
    """
    return render_template("account/register.html")


@bp.post("/register")
def register():
    print(request)
    user = None
    response_json = None
    if request.is_json:
        body = request.get_json()
        user = User.from_json(body)
        # user = User(**body)
        user.id = _find_next_id()
        accounts.append(user)
        # response_json = ResponseEntity.build_response_json(HTTPStatus.CREATED, user)
        response_json = user.json()
    else:
        response_json = ResponseEntity.build_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, entity=user,
                                                      message="Invalid JSON object!")

    return make_response(response_json)


# login to an account
@bp.get("/login")
def login_view():
    """
    login to an account
    """
    return render_template("account/login.html")


@bp.post("/login")
def login():
    print(request)
    if request.is_json:
        user = request.get_json()
        print(f"user:{user}")
        if not accounts:
            for account in accounts:
                if account['user_name'] == user.user_name:
                    return make_response(HTTPStatus.OK, account)

    response = ErrorEntity.error(HTTPStatus.NOT_FOUND, "Account is not registered!")
    print(response)

    return make_response(response)


# view profile
@bp.get("/profile")
def profile_view():
    """
    view profile
    """
    return render_template("account/profile.html")


# forgot-password
@bp.get("/forgot-password")
def forgot_password():
    """
    forgot-password
    """
    return render_template("account/forgot-password.html")


# Logout Page
@bp.post("/logout")
def logout():
    """
    About Us Page
    """
    # return render_template("index.html")
    return redirect(url_for('iws.webapp.index'))


# accounts home page
@bp.get("/notifications")
def notifications():
    """
    Services Page
    """
    return render_template("account/notifications.html")
