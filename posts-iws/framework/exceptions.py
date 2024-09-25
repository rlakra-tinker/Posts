#
# Author: Rohtash Lakra
#

class DuplicateRecordException(BaseException):
    """ Duplicate Record exception """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        return DuplicateRecordException("Record already exists!")


class NoRecordFoundException(BaseException):
    """ Duplicate Record exception """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        return NoRecordFoundException("Record doesn't exist!")

