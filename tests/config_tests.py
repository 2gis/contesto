import os
import unittest

from contesto import config
from contesto.utils.lambda_object import LambdaObject


class ConfigTest(unittest.TestCase):
    def test_default_config(self):
        default = LambdaObject()
        default.selenium = {
            "host": "localhost",
            "port": 4444,
            "browser": "firefox",
            "platform": "ANY",
        }
        default.timeout = {"normal": 5, }
        default.session = {"shared": False, }

        for key, value in vars(default).items():
            for k, v in value.items():
                actual = getattr(config, key)[k]
                expected = v
                assert type(actual) == type(expected)
                assert actual == expected

    def test_override_params(self):
        ### @todo mock config files (data/config/*.ini)
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/override.ini")
        self.assertEqual("ie", config.selenium["browser"])

    def test_add_params(self):
        ### @todo mock config files (data/config/*.ini)
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/addition.ini")
        self.assertEqual(30, config.timeout["max"])
        self.assertEqual("value", config.section["param"])

    def test_complex_param(self):
        ### @todo mock config files (data/config/*.ini)
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/complex.ini")
        self.assertEqual(42, config.complex["int"])
        self.assertEqual(2.718, config.complex["float"])
        self.assertEqual("3.14", config.complex["string"])
        self.assertIs(True, config.complex["bool"])
        self.assertEqual({"a": 1, "b": 2}, config.complex["dict"])
        self.assertEqual([1, 2, 3], config.complex["list"])
        self.assertEqual("", config.complex["empty_string"])
