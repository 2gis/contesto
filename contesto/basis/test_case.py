import logging
from urllib2 import URLError

from contesto import config
from contesto.core.driver import ContestoDriver
from contesto.exceptions import ConnectionError
from contesto.utils.log import log_handler

from unittest import TestCase


class ContestoTestCase(object):

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

    def _teardown_test(self):
        if not config.session["shared"]:
            self._destroy_session(self)

    @staticmethod
    def _create_session(cls):
        """
        :rtype: ContestoDriver
        :raise: UnknownBrowserName
        :raise: ConnectionError
        """
        try:
            cls.driver_settings = getattr(config, cls._driver_type)
        except AttributeError:
            # for backward compatibility: HttpDriver mixin if no mixin provided
            from .driver_mixin import HttpDriver
            d = dict(cls.__dict__.items() + HttpDriver.__dict__.items())
            cls.__class__.__bases__ += (HttpDriver, )
            cls.driver_settings = getattr(config, cls._driver_type)

        desired_capabilities = cls._form_desired_capabilities(cls.driver_settings)

        try:
            command_executor = "http://%s:%d/wd/hub" % (cls.driver_settings["host"], cls.driver_settings["port"])
            return ContestoDriver(command_executor=command_executor, desired_capabilities=desired_capabilities)
        except URLError:
            raise ConnectionError(cls.driver_settings["host"], cls.driver_settings["port"])

    @staticmethod
    def _destroy_session(cls):
        """
        :raise: ConnectionError
        """
        try:
            cls.driver.quit()
        except URLError:
            raise ConnectionError(cls.driver_settings["host"], cls.driver_settings["port"])


class UnittestContestoTestCase(ContestoTestCase, TestCase):
    @classmethod
    def setUpClass(cls):
        super(UnittestContestoTestCase, cls)._setup_class()

    @classmethod
    def tearDownClass(cls):
        super(UnittestContestoTestCase, cls)._teardown_class()

    def setUp(self):
        super(UnittestContestoTestCase, self)._setup_test()

    def tearDown(self):
        super(UnittestContestoTestCase, self)._teardown_test()


class PyTestContestoTestCase(ContestoTestCase):
    @classmethod
    def setup_class(cls):
        super(PyTestContestoTestCase, cls)._setup_class()

    @classmethod
    def teardown_class(cls):
        super(PyTestContestoTestCase, cls)._teardown_class()

    def setup_method(self, method):
        super(PyTestContestoTestCase, self)._setup_test()

    def teardown_method(self, method):
        super(PyTestContestoTestCase, self)._teardown_test()


# for backward compatibility
BaseTestCase = PyTestContestoTestCase
