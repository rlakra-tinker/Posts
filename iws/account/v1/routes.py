#
# Author: Rohtash Lakra
#
from iws.framework.http import HTTPMethod
from . import bp as v1_account


@v1_account.route('/', methods=[HTTPMethod.POST])
def create_account():
    # Creates a new account
    pass
