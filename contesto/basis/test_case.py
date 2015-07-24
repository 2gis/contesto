import logging
from urllib2 import URLError
import unittest

from contesto import config
from contesto.core.driver import Driver
from contesto.exceptions import ConnectionError
from contesto.utils.log import log_handler, log
from .driver_mixin import SeleniumDriverMixin

try:
    from browsermobproxy import Client as BMPClient
except ImportError:
    BMPClient = None


class ContestoTestCase(unittest.TestCase):
    def __new__(cls, *args, **kwargs):
        try:
            cls.driver_settings = getattr(config, cls.driver_section)
        except AttributeError:
            # for backward compatibility: SeleniumDriverMixin mixin if no mixin provided
            if isinstance(cls, type):
                cls.__bases__ += (SeleniumDriverMixin, )
            else:
                cls.__class__.__bases__ += (SeleniumDriverMixin, )
            cls.driver_settings = getattr(config, cls.driver_section)
        cls.desired_capabilities = cls._form_desired_capabilities(cls.driver_settings)
        cls.command_executor = cls._form_command_executor(cls.driver_settings)
        return super(ContestoTestCase, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def _setup_class(cls):
        if config.session["shared"]:
            cls.driver = cls._create_session(cls)

    @classmethod
    def _teardown_class(cls):
        if config.session["shared"]:
            cls._destroy_session(cls)

    def _setup_test(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")
        logger.addHandler(log_handler)
        if not config.session["shared"]:
            self.driver = self._create_session(self)
        self.driver._testMethodName = self._testMethodName
        log.env("sessionId: %s", self.driver.session_id)
        log.env("capabilities: \n%s\n" % self.driver.capabilities)

    def _teardown_test(self):
        if not config.session["shared"]:
            self._destroy_session(self)

    @classmethod
    def _connect_to_proxy(cls):
        if config.browsermobproxy['enabled']:
            if BMPClient is not None:
                cls.bmproxy = BMPClient(config.browsermobproxy['url'])
                cls.bmproxy.webdriver_proxy().add_to_capabilities(cls.desired_capabilities)
            else:
                raise ImportError('Cannot import name browsermobproxy.')

    @classmethod
    def _disconnect_from_proxy(cls):
        if config.browsermobproxy['enabled']:
            cls.bmproxy.close()

    @staticmethod
    def _create_session(cls):
        """
        :rtype: Driver
        """
        cls._connect_to_proxy()
        return cls._start_driver(cls.desired_capabilities, cls.command_executor)

    @staticmethod
    def _form_command_executor(driver_settings):
        host = driver_settings["host"]
        port = driver_settings["port"]
        if "prefix" in driver_settings.keys():
            prefix = driver_settings["prefix"].strip()
            if len(prefix) > 0 and not prefix.startswith('/'):
                prefix = '/' + prefix
        else:
            prefix = '/wd/hub'
        command_executor = "http://%s:%d/%s" % (host, port, prefix.strip('/'))
        return command_executor.rstrip('/')

    @classmethod
    def _start_driver(cls, desired_capabilities, command_executor):
        """
        :raise: ConnectionError
        """
        try:
            log.init("starting session...")
            driver = cls.driver_class(
                command_executor=command_executor,
                desired_capabilities=desired_capabilities)
            return driver
        except URLError:
            raise ConnectionError(command_executor)

    @staticmethod
    def _destroy_session(cls):
        """
        :raise: ConnectionError
        """
        cls._disconnect_from_proxy()
        try:
            cls.driver.quit()
        except URLError:
            raise ConnectionError('%s:%s' % (cls.driver_settings["host"], cls.driver_settings["port"]))

    @classmethod
    def setUpClass(cls):
        cls._setup_class()

    @classmethod
    def tearDownClass(cls):
        cls._teardown_class()

    def setUp(self):
        self._setup_test()

    def tearDown(self):
        self._teardown_test()

    @classmethod
    def setup_class(cls):
        cls._setup_class()

    @classmethod
    def teardown_class(cls):
        cls._teardown_class()

    def setup_method(self, method):
        self._setup_test()

    def teardown_method(self, method):
        self._teardown_test()

# for backward compatibility
UnittestContestoTestCase = ContestoTestCase
PyTestContestoTestCase = ContestoTestCase
BaseTestCase = ContestoTestCase
