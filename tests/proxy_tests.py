from contesto.basis.driver_mixin import HttpDriver
from contesto import config
from selenium.webdriver import Proxy
from mock import patch
import os
import unittest

try:
    from browsermobproxy import Client as BMPClient
except ImportError:
    BMPClient = None


class ProxyInDesireCapabilitiesTestCase(unittest.TestCase):
    def setUp(self):
        ### @todo mock config files (data/config/*.ini)
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/dc_with_proxy.ini")

    @patch(__name__ + '.BMPClient')
    def test_proxy_in_desired_capabilities(self, MockClient):
        proxy_host = config.browsermobproxy['url'].split(':')[0] + ':' + '9091'
        proxy_params = {
            'proxy': {
                'proxyType': 'MANUAL',
                'sslProxy': proxy_host,
                'httpProxy': proxy_host
            }
        }

        driver = HttpDriver()

        instance = MockClient.return_value
        instance.proxy = proxy_host

        HttpDriver.bmproxy = BMPClient(config.browsermobproxy['url'])
        HttpDriver.dc_from_config = None

        HttpDriver.bmproxy.webdriver_proxy.return_value = Proxy({
            "httpProxy": HttpDriver.bmproxy.proxy,
            "sslProxy": HttpDriver.bmproxy.proxy,
        })

        dc_params = getattr(config, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(dc_params)
        self.assertDictEqual(desired_capabilities['proxy'], proxy_params['proxy'])

    def tearDown(self):
        config.browsermobproxy['enabled'] = 0