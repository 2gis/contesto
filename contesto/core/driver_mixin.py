from contesto.exceptions import UnknownBrowserName
from selenium.webdriver import DesiredCapabilities

from contesto.core.driver import ContestoWebDriver, ContestoMobileDriver


class AbstractDriverMixin(object):
    driver_section = None
    driver_class = None
    _loaded_dc = None
    _loaded_settings = None

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        cls._loaded_dc = driver_settings.get("desired_capabilities", None)
        if cls._loaded_dc is None:
            cls._loaded_settings = {
                key: value for key, value in driver_settings.items()
                if key not in ('host', 'port')}

        return cls._loaded_dc if cls._loaded_dc else cls._loaded_settings


class SeleniumDriverMixin(AbstractDriverMixin):
    driver_section = 'selenium'
    driver_class = ContestoWebDriver

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

        if cls._loaded_dc:
            return cls._loaded_dc

        try:
            desired_capabilities = cls.capabilities_map[driver_settings["browser"].lower()]
            desired_capabilities.update(cls._loaded_settings)
        except KeyError:
            raise UnknownBrowserName(driver_settings.selenium["browser"], cls.capabilities_map.keys())

        return desired_capabilities


class QtWebkitDriverMixin(AbstractDriverMixin):
    driver_section = 'qtwebkitdriver'
    driver_class = ContestoWebDriver


class IosDriverMixin(AbstractDriverMixin):
    driver_section = 'iosdriver'
    driver_class = ContestoMobileDriver


class AndroidDriverMixin(AbstractDriverMixin):
    driver_section = 'androiddriver'
    driver_class = ContestoMobileDriver
