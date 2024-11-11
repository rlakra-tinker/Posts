#
# Author: Rohtash Lakra
#
import logging
import os
import re
import sys
import time
import traceback

import requests

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

    @staticmethod
    def abs_path(file_name) -> str:
        """Returns the absolute path of the given file."""
        return os.path.abspath(os.path.dirname(file_name))

    @staticmethod
    def exists(path) -> bool:
        """Returns true if the path exists otherwise false."""
        return os.path.exists(path)

    @staticmethod
    def measure_ttfb(url):
        logger.debug(f"+measure_ttfb({url})")
        _watcher = StopWatch()
        _watcher.start()
        response = requests.get(url)
        _watcher.stop()
        elapsed = _watcher.elapsed()
        logger.debug(f"elapsed={elapsed}")
        ttfb = elapsed * 1000  # Convert to milliseconds

        logger.debug(f"-measure_ttfb(), url={url}, ttfb={ttfb}")
        return ttfb


class StopWatch(object):
    """Test support functionality for other tests."""

    def __init__(self):
        self.start_time = None
        self.duration = None

    def start(self):
        self.start_time = self.now()
        self.duration = None

    def stop(self):
        self.duration = self.now() - self.start_time

    @staticmethod
    def now():
        return time.time()

    # @property
    def elapsed(self):
        assert self.start_time is not None
        return self.now() - self.start_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
