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
