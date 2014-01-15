from contesto.basis.driver_mixin import HttpDriver, IosDriver,QtWebkitDriver
from contesto import config

import os
import unittest

class DesireCapabilitiesTestCase(unittest.TestCase):

    def setUp(self):
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/drivers.ini")

    def test_ios_driver(self):
        driver = IosDriver()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        assert desired_capabilities["device"] == "iPhone Simulator"
        assert desired_capabilities["platform"] == "Mac"
        assert desired_capabilities["app"] == "/Users/test/app.app"
        assert desired_capabilities["version"] == 7.0

    def test_http_driver(self):
        driver = HttpDriver()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        assert desired_capabilities["browser"] == "firefox"
        assert desired_capabilities["platform"] == "ANY"

    def test_qtwebkit_driver(self):
        driver = QtWebkitDriver()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        assert desired_capabilities["app"] == "/Users/test/app"
