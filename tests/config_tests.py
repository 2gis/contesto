import os

from contesto import config
from contesto.utils.lambda_object import LambdaObject


def test_default_config():
    default = LambdaObject()
    default.selenium = {
        "host": "localhost",
        "port": 4444,
        "browser": "firefox",
        "platform": "ANY",
    }
    default.timeout = {"normal": 5, }
    default.session = {"shared": False, }

    for key, value in vars(default).iteritems():
        for k, v in value.iteritems():
            actual = getattr(config, key)[k]
            expected = v
            assert type(actual) == type(expected)
            assert actual == expected


def test_override_params():
    ### @todo mock config files (data/config/*.ini)
    config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/override.ini")
    assert config.selenium["browser"] == "ie"


def test_add_params():
    ### @todo mock config files (data/config/*.ini)
    config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/addition.ini")
    assert config.timeout["max"] == 30
    assert config.section["param"] == "value"


def test_complex_param():
    ### @todo mock config files (data/config/*.ini)
    config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/complex.ini")
    assert config.complex["int"] == 42
    assert config.complex["float"] == 2.718
    assert config.complex["string"] == "3.14"
    assert config.complex["bool"] is True
    assert config.complex["dict"] == {"a": 1, "b": 2}
    assert config.complex["list"] == [1, 2, 3]
    assert config.complex["empty_string"] == str()