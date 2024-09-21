#
# Author: Rohtash Lakra
#
import json

from flask import Blueprint, make_response, request, session, g, redirect, url_for
from framework.http import HTTPStatus
from framework.model.abstract import ErrorEntity, ResponseEntity
from rest.contact.service import ContactService
from rest.contact.models import Contact

#
bp = Blueprint("contacts", __name__, url_prefix="/contacts")
"""
Making a Flask Blueprint and registering it in an application, you extend the application with its contents.
"""

# account's service
contactService = ContactService()


@bp.post("/")
def create():
    print(f"request => {request}")
    if request.is_json:
        body = request.get_json()
        print(f"body => {body}")
        first_name = body.get('first_name', None)
        last_name = body.get('last_name', None)
        country = body.get('country', None)
        subject = body.get('subject', None)
        # contact = Contact.model_extra(request.get_json())
        contact = Contact.create(first_name, last_name, country, subject)
    elif request.form:
        print(f"request.form => {request.form}")
        # first_name, last_name, country, subject
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        country = request.form.get('country')
        subject = request.form.get('subject')
        contact = Contact.create(first_name, last_name, country, subject)

    errors = contactService.validate(contact)
    print(f"errors => {json.dumps(errors)}")

    response = None
    if not errors:
        try:
            contact = contactService.create(contact)
            response = ResponseEntity.build_response(HTTPStatus.CREATED, entity=contact,
                                                     message="Contact is successfully created.")
        except Exception as ex:
            message = f"Contact={contact.first_name} is already registered! ex:{ex}"
            error = ErrorEntity.error(HTTPStatus.INTERNAL_SERVER_ERROR, message, exception=ex)
            response = ResponseEntity.build_response(HTTPStatus.INTERNAL_SERVER_ERROR, error, exception=ex)
        # else:
        #     return redirect(url_for("iws.rest.v1.contacts.create"))
    else:
        response = errors

    print(f"response ==> {response}")
    # return make_response(response)
    return redirect(url_for("iws.webapp.contact"))

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
    print(json.dumps(response))

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
