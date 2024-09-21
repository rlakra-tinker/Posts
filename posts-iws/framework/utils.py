#
# Author: Rohtash Lakra
#
import sys
import traceback

from framework.enums import AutoName


class Utils(AutoName):

    @staticmethod
    def stack_trace(exception: Exception):
        """Returns the string representation of exception"""
        exc_info = sys.exc_info()
        return ''.join(traceback.format_exception(*exc_info))

    @staticmethod
    def exception(exception:Exception, message:str):
        return exception(message)
