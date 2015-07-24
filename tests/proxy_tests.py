from contesto import config
from mock import patch
import os
import unittest

from contesto.basis import test_case
from contesto.basis.test_case import ContestoTestCase
from contesto.basis.driver_mixin import SeleniumDriverMixin


class ProxyInDesireCapabilitiesTestCase(unittest.TestCase):
    proxy_host = "http://localhost:9091"

    def setUp(self):
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/dc_with_proxy.ini")

    def test_proxy_adding_in_desired_capabilities_with_config(self):
        driver = SeleniumDriverMixin()
        driver_settings = getattr(config, driver.driver_section)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        ContestoTestCase.desired_capabilities = desired_capabilities
        with patch.object(test_case.BMPClient, '__init__', return_value=None):
            test_case.BMPClient.proxy = self.proxy_host
            ContestoTestCase._connect_to_proxy()

        proxy_params = {
            'proxy': {
                'proxyType': 'MANUAL',
                'sslProxy': self.proxy_host,
                'httpProxy': self.proxy_host
            }
        }
        self.assertDictEqual(ContestoTestCase.desired_capabilities['proxy'], proxy_params['proxy'])

    def tearDown(self):
        config.browsermobproxy['enabled'] = 0


class ProxyDisabledInDesireCapabilitiesTestCase(unittest.TestCase):
    proxy_host = "http://localhost:9091"

    def test_proxy_disabled_in_desired_capabilities_by_default(self):
        driver = SeleniumDriverMixin()
        driver_settings = getattr(config, driver.driver_section)
        desired_capabilities = driver._form_desired_capabilities(driver_settings)
        ContestoTestCase.desired_capabilities = desired_capabilities
        with patch.object(test_case.BMPClient, '__init__', return_value=None):
            test_case.BMPClient.proxy = self.proxy_host
            ContestoTestCase._connect_to_proxy()

        self.assertEqual(None, ContestoTestCase.desired_capabilities.get('proxy', None),
                         ContestoTestCase.desired_capabilities.get('proxy'))