#
# Author: Rohtash Lakra
#
import sys
import traceback
import logging
import re
from framework.enums import BaseEnum

# logger
logger = logging.getLogger(__name__)

# Upper-case letters
CAPITALS = re.compile('([A-Z])')


class Utils(BaseEnum):

    @staticmethod
    def stack_trace(exception: Exception):
        """Returns the string representation of exception"""
        exc_info = sys.exc_info()
        return ''.join(traceback.format_exception(*exc_info))

    @staticmethod
    def exception(exception: Exception, message: str):
        return exception(message)

    @staticmethod
    def camel_case_to_pep8(text):
        """Convert a camel cased text to PEP8 style."""
        converted = CAPITALS.sub(lambda m: '_' + m.groups()[0].lower(), text)
        if converted[0] == '_':
            return converted[1:]
        else:
            return converted

    @staticmethod
    def pep8_to_camel_case(text, initial=False):
        """Convert a PEP8 style text to camel case."""
        chunks = text.split('_')
        converted = [s[0].upper() + s[1:].lower() for s in chunks]
        if initial:
            return ''.join(converted)
        else:
            return chunks[0].lower() + ''.join(converted[1:])

