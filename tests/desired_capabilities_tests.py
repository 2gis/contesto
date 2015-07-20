from contesto.basis.driver_mixin import SeleniumDriverMixin,\
    IosDriverMixin, QtWebkitDriverMixin
from contesto import config
from contesto.basis.test_case import ContestoTestCase

import os
import unittest


class DesireCapabilitiesTestCase(unittest.TestCase):
    def setUp(self):
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/drivers.ini")

    def test_dc_loading_any_additional_setting(self):
        driver = SeleniumDriverMixin()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        self.assertEqual(desired_capabilities.get('additional_setting'), 'some_value',
                         'should load any setting to desired_capabilities')

    def test_ios_driver(self):
        driver = IosDriverMixin()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        self.assertEqual(desired_capabilities["device"], "iPhone Simulator", 'wrong device in capabilities in iosdriver')
        self.assertEqual(desired_capabilities["platform"], "Mac", 'wrong platform in capabilities in iosdriver')
        self.assertEqual(desired_capabilities["app"], "/Users/test/app.app", 'wrong app in capabilities in iosdriver')
        self.assertEqual(desired_capabilities["version"], 7.0, 'wrong version in capabilities in iosdriver')

    def test_http_driver(self):
        driver = SeleniumDriverMixin()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        self.assertEqual(desired_capabilities["browserName"], "firefox", 'wrong browser in capabilities in httpdriver')
        self.assertEqual(desired_capabilities["version"], "", 'wrong version in capabilities in httpdriver')
        self.assertEqual(desired_capabilities["platform"], "ANY", 'wrong platform in capabilities in httpdriver')

    def test_qtwebkit_driver(self):
        driver = QtWebkitDriverMixin()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        self.assertEqual(desired_capabilities["app"], "/Users/test/app", 'wrong platform in capabilities in qtwebkitdriver')


class DictionaryDesireCapabilitiesTestCase(unittest.TestCase):
    def setUp(self):
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/desired_capabilities.ini")

    def test_dictionary_desired_capabilities_overwrite_all_other_capabilities(self):
        dc = {
            "browserName": "firefox",
            "platform": "LINUX"
        }
        driver = SeleniumDriverMixin()
        driver_settings = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        self.assertEqual(desired_capabilities, dc)

    def tearDown(self):
        del config.selenium['desired_capabilities']


class DesiredWebDriverPrefixTestCase(unittest.TestCase):
    def setUp(self):
        self.common_driver_settings = {'host': 'localhost', 'port': 4444}
        host = self.common_driver_settings['host']
        port = self.common_driver_settings['port']
        self.common_url = "http://%s:%d" % (host, port)

    def test_default_prefix(self):
        driver_settings = self.common_driver_settings
        command_executor = ContestoTestCase._form_command_executor(driver_settings)
        self.assertEqual(self.common_url + '/wd/hub', command_executor)

    def test_empty_prefix(self):
        driver_settings = self.common_driver_settings
        driver_settings['prefix'] = str()
        command_executor = ContestoTestCase._form_command_executor(driver_settings)
        self.assertEqual(self.common_url, command_executor)

    def test_custom_prefix(self):
        driver_settings = self.common_driver_settings
        driver_settings['prefix'] = 'test'
        command_executor = ContestoTestCase._form_command_executor(driver_settings)
        self.assertEqual(self.common_url + '/test', command_executor)