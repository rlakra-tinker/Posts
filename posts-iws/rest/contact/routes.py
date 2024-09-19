#
# Author: Rohtash Lakra
#
from flask import Blueprint, make_response, request, session, g, redirect, url_for
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity
from rest.contact.service import ContactService
from .models import Contact

#
bp = Blueprint("contact", __name__, url_prefix="/contact")
"""
Making a Flask Blueprint and registering it in an application, you extend the application with its contents.
"""


# account's service
contactService = ContactService()

@bp.post("/register")
def register():
    print(request)
    if request.is_json:
        contact = Contact.model_construct(request.get_json())
        contactService.add(contact)
        return contact, 201
    else:
        # first_name, last_name, country, subject
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        country = request.form['country']
        subject = request.form['subject']
        contact = Contact(first_name=first_name, last_name=last_name, country=country, subject=subject)
        error = contactService.validate(contact)

        # db = get_db()
        response = None
        if error is None:
            try:
                response = contactService.addContact(first_name, last_name, country, subject)
            except Exception as ex:
                error = f"Contact '{contact}' is already registered! ex:{ex}"
            else:
                return redirect(url_for("iws.rest.v1.contact.register"))

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

    response = ErrorEntity.get_error(HTTPStatus.NOT_FOUND, "Account is not registered!")
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
