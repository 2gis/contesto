# coding: utf-8
from types import MethodType
try:
    from urllib2 import URLError
except ImportError:
    from urllib.error import URLError
import unittest

from contesto.core.driver import Driver
from contesto.core.driver_mixin import SeleniumDriverMixin

from contesto.exceptions import ConnectionError
from contesto.step import Steps
from contesto.utils.error_handler import collect_on_error
from contesto.utils.screenshot import save_screenshot_on_error
from contesto.utils.log import log
from contesto.globals import _context

from contesto import config

try:
    from browsermobproxy import Client as BMPClient
except ImportError:
    BMPClient = None


def _wrap(instance, attr_name, decorator):
    attr = getattr(instance, attr_name)
    if isinstance(attr, MethodType):
        func = decorator(attr.__func__)
        setattr(instance, attr_name, MethodType(func, instance))
    else:
        setattr(instance, attr_name, decorator(attr))


class ContestoTestCase(unittest.TestCase):
    def __init__(self, test_name='runTest'):
        super(ContestoTestCase, self).__init__(test_name)
        self._meta_info = dict(
            name=str(self._testMethodName),
            class_name='%s.%s' % (self.__class__.__module__,
                                  self.__class__.__name__),
            steps=Steps(),
            attachments=[]
        )
        if config.utils.get('save_screenshots'):
            _wrap(self, test_name, save_screenshot_on_error)

    def __new__(cls, test_name='runTest'):
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
        return super(ContestoTestCase, cls).__new__(cls)

    def run(self, result=None):
        self._init_context()
        try:
            if config.utils.get('collect_metadata'):
                setattr(self, "setUp", collect_on_error(self.setUp))
                setattr(self, "tearDown", collect_on_error(self.tearDown))
                _wrap(self, self._testMethodName, collect_on_error)
            super(ContestoTestCase, self).run(result)
        finally:
            self._free_context()

    @classmethod
    def _setup_class(cls):
        if config.session["shared"]:
            cls.driver = cls._create_session(cls)

    @classmethod
    def _teardown_class(cls):
        if config.session["shared"]:
            cls._destroy_session(cls)

    def _init_context(self):
        _context.test = self

    def _free_context(self):
        _context.test = None

    def _setup_test(self):
        if not config.session["shared"]:
            self.driver = self._create_session(self)
        self.driver._testMethodName = self._testMethodName
        log.info("sessionId: %s", self.driver.session_id)
        log.info("capabilities: %s" % self.driver.capabilities)

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
            log.info("starting session...")
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

UnittestContestoTestCase = ContestoTestCase
BaseTestCase = ContestoTestCase
