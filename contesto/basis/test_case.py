import logging
from urllib2 import URLError

from selenium.webdriver import DesiredCapabilities

from contesto import config
from contesto.core.driver import ContestoDriver
from contesto.core.exceptions import UnknownBrowserName, ConnectionError
from contesto.utils.log import log_handler


class BaseTestCase(object):
    capabilities_map = {
        "firefox": DesiredCapabilities.FIREFOX,
        "internetexplorer": DesiredCapabilities.INTERNETEXPLORER,
        "chrome": DesiredCapabilities.CHROME,
        "opera": DesiredCapabilities.OPERA,
        "safari": DesiredCapabilities.SAFARI,
        "htmlunit": DesiredCapabilities.HTMLUNIT,
        "htmlunitjs": DesiredCapabilities.HTMLUNITWITHJS,
        "iphone": DesiredCapabilities.IPHONE,
        "ipad": DesiredCapabilities.IPAD,
        "android": DesiredCapabilities.ANDROID,
        "phantomjs": DesiredCapabilities.PHANTOMJS,
        ### aliases:
        "ff": DesiredCapabilities.FIREFOX,
        "internet explorer": DesiredCapabilities.INTERNETEXPLORER,
        "iexplore": DesiredCapabilities.INTERNETEXPLORER,
        "ie": DesiredCapabilities.INTERNETEXPLORER,
        "phantom": DesiredCapabilities.PHANTOMJS,
    }

    @classmethod
    def setup_class(cls):
        if bool(int(config.session["shared"])):
            cls.driver = cls._create_session(cls)

    @classmethod
    def teardown_class(cls):
        if bool(int(config.session["shared"])):
            cls._destroy_session(cls)

    def setup_method(self, method):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")
        logger.addHandler(log_handler)
        if not bool(int(config.session["shared"])):
            self.driver = self._create_session(self)

    def teardown_method(self, method):
        if not bool(int(config.session["shared"])):
            self._destroy_session(self)

    @staticmethod
    def _create_session(cls):
        """
        :rtype: ContestoDriver
        :raise: UnknownBrowserName
        :raise: ConnectionError
        """
        try:
            command_executor = "http://%s:%s/wd/hub" % (config.selenium["host"], config.selenium["port"])
            desired_capabilities = cls.capabilities_map[config.selenium["browser"].lower()]
            return ContestoDriver(command_executor=command_executor, desired_capabilities=desired_capabilities)
        except KeyError:
            raise UnknownBrowserName(config.selenium["browser"], cls.capabilities_map.keys())
        except URLError:
            raise ConnectionError(config.selenium["host"], config.selenium["port"])

    @staticmethod
    def _destroy_session(cls):
        """
        :raise: ConnectionError
        """
        try:
            cls.driver.quit()
        except URLError:
            raise ConnectionError(config.selenium["host"], config.selenium["port"])
        except AttributeError:
            pass
