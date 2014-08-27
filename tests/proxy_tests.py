from contesto.basis.driver_mixin import HttpDriver
from contesto import Config
from selenium.webdriver import Proxy
from mock import patch
import os
import unittest

try:
    from browsermobproxy import Client as BMPClient
except ImportError:
    BMPClient = None


class ProxyInDesireCapabilitiesTestCase(unittest.TestCase):
    cfg = Config()
    ### @todo mock config files (data/config/*.ini)
    cfg.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/dc_with_proxy.ini")

    @patch(__name__ + '.BMPClient')
    def test_proxy_in_desired_capabilities(self, MockClient):
        proxy_host = self.cfg.browsermobproxy['url'].split(':')[0] + ':' + '9091'
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

        HttpDriver.bmproxy = BMPClient(self.cfg.browsermobproxy['url'])

        HttpDriver.bmproxy.webdriver_proxy.return_value = Proxy({
            "httpProxy": HttpDriver.bmproxy.proxy,
            "sslProxy": HttpDriver.bmproxy.proxy,
        })

        dc_params = getattr(self.cfg, driver._driver_type)
        desired_capabilities = driver._form_desired_capabilities(dc_params)
        self.assertDictEqual(desired_capabilities['proxy'], proxy_params['proxy'])