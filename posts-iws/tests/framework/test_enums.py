import unittest

from framework.enums import AutoName, AutoNameUpperCase


class EnumsTest(unittest.TestCase):
    """Unit-tests for Enums"""

    def test_auto_name_enum(self):
        print("test_auto_name_enum")
        self.assertEqual("<enum 'AutoName'>", str(AutoName))
        print()

    def test_auto_name_upper_case_enum(self):
        print("test_auto_name_upper_case_enum")
        self.assertEqual("<enum 'AutoNameUpperCase'>", str(AutoNameUpperCase))
        # self.assertEqual(('CONSUMER', 'EXPERT'), RoleEnum.names())
        # self.assertEqual(('consumer', 'service_provider'), RoleEnum.values())
        # text = 'expert'
        # expected = 'RoleEnum <EXPERT=service_provider>'
        # print(f"{text} of_name={RoleEnum.of_name(text)}")
        # self.assertEqual(expected, str(RoleEnum.of_name(text)))
        # self.assertTrue(RoleEnum.equals(RoleEnum.EXPERT, text))
        #
        # text = 'service_provider'
        # print(f"{text} of_value={RoleEnum.of_value(text)}")
        # self.assertEqual(expected, str(RoleEnum.of_value(text)))
        # self.assertTrue(RoleEnum.equals(RoleEnum.EXPERT, text))
        print()


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
