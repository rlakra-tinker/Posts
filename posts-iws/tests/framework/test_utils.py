#
# Author: Rohtash Lakra
#
from framework.utils import Utils
from tests.framework.utils import AbstractTestCase


class UtilsTest(AbstractTestCase):

    def test_stack_trace(self):
        print('test_stack_trace()')
        error = ValueError('validation error message!')
        stack_trace = Utils.stack_trace(error)
        print(f"stack_trace={stack_trace}")
        self.assertIsNotNone(stack_trace)
        print()

    def test_exception(self):
        print('test_exception()')
        try:
            raise Utils.exception(ValueError, 'A validation error message!')
        except ValueError as ex:
            print(f"ex={ex}")
            self.assertIsNotNone(ex)
        print()
