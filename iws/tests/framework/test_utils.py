#
# Author: Rohtash Lakra
#
from framework.utils import Utils
from tests.base import AbstractTestCase


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

    def test_camel_case_to_pep8(self):
        def check(lower_cc, upper_cc, correct):
            x1 = Utils.camel_case_to_pep8(lower_cc)
            x2 = Utils.camel_case_to_pep8(upper_cc)
            assert correct == x1
            assert correct == x2

            y1 = Utils.pep8_to_camel_case(x1, True)
            y2 = Utils.pep8_to_camel_case(x2, False)
            assert upper_cc == y1
            assert lower_cc == y2

        examples = [('foo', 'Foo', 'foo'),
                    ('fooBar', 'FooBar', 'foo_bar'),
                    ('fooBarBaz', 'FooBarBaz', 'foo_bar_baz'),
                    ('fOO', 'FOO', 'f_o_o'),
                    ('rohtashLakra', 'RohtashLakra', 'rohtash_lakra')]

        for a, b, c in examples:
            check(a, b, c)

    def test_measure_ttfb(self):
        print('test_measure_ttfb()')
        url = "https://www.google.com/"
        ttfb = Utils.measure_ttfb(url)
        print(f"TTFB for {url}: {ttfb:.2f} ms, {ttfb / 1000:.2f} seconds")
        self.assertIsNotNone(ttfb)
        self.assertGreaterEqual(ttfb, 1)
        print()
