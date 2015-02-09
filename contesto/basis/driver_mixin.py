from contesto.exceptions import UnknownBrowserName
from selenium.webdriver import DesiredCapabilities

from contesto.core.driver import WebContestoDriver, MobileContestoDriver


class AbstractDriver(object):
    _driver_type = None
    _driver = None
    loaded_dc = None
    loaded_settings = None

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        cls.loaded_dc = driver_settings.get("desired_capabilities", None)
        if cls.loaded_dc is None:
            cls.loaded_settings = {
                key: value for key, value in driver_settings.iteritems()
                if key not in ('host', 'port')}

        return cls.loaded_dc if cls.loaded_dc else cls.loaded_settings


class SeleniumDriverMixin(AbstractDriver):
    _driver_type = 'selenium'
    _driver = WebContestoDriver

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
    def _form_desired_capabilities(cls, driver_settings):
        """
        :raise: UnknownBrowserName
        """
        super(SeleniumDriverMixin, cls)._form_desired_capabilities(driver_settings)

        if cls.loaded_dc:
            return cls.loaded_dc

        try:
            desired_capabilities = cls.capabilities_map[driver_settings["browser"].lower()]
            desired_capabilities.update(cls.loaded_settings)
        except KeyError:
            raise UnknownBrowserName(driver_settings.selenium["browser"], cls.capabilities_map.keys())

        return desired_capabilities


class QtWebkitDriverMixin(AbstractDriver):
    _driver_type = 'qtwebkitdriver'
    _driver = WebContestoDriver


class IosDriverMixin(AbstractDriver):
    _driver_type = 'iosdriver'
    _driver = MobileContestoDriver


class AndroidDriverMixin(AbstractDriver):
    _driver_type = 'androiddriver'
    _driver = MobileContestoDriver
