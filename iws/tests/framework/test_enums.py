import unittest

from framework.enums import BaseEnum, AutoNameUpperCase, AutoNameLowerCase, EnvType


class EnumsTest(unittest.TestCase):
    """Unit-tests for Enums"""

    def test_base_enum(self):
        print("test_base_enum")
        self.assertEqual("<enum 'BaseEnum'>", str(BaseEnum))
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

    def test_auto_name_lower_case_enum(self):
        print("test_auto_name_lower_case_enum")
        self.assertEqual("<enum 'AutoNameLowerCase'>", str(AutoNameLowerCase))
        print()

    def test_env_type_enum(self):
        print("test_env_type_enum")
        self.assertEqual("<enum 'EnvType'>", str(EnvType))

        expected = ('DEVELOPMENT', 'PRODUCTION', 'STAGING', 'TESTING')
        self.assertEqual(expected, EnvType.names())
        self.assertEqual(expected, EnvType.values())

        text = 'testing'
        expected = 'EnvType <TESTING=TESTING>'
        print(f"{text} of_name={EnvType.of_name(text)}")
        self.assertEqual(expected, str(EnvType.of_name(text)))
        self.assertTrue(EnvType.equals(EnvType.TESTING, text))

        text = 'TESTING'
        print(f"{text} of_value={EnvType.of_value(text)}")
        self.assertEqual(expected, str(EnvType.of_value(text)))
        self.assertTrue(EnvType.equals(EnvType.TESTING, text))

        flask_env = EnvType.flask_env()
        print(f"flask_env={flask_env}")
        if flask_env is not None:
            self.assertEqual(flask_env.lower(), EnvType.of_name(flask_env).name.lower())


# Starting point
if __name__ == 'main':
    unittest.main(exit=False)
