from contesto.exceptions import UnknownBrowserName
from selenium.webdriver import DesiredCapabilities
from contesto import config


class AbstractDriver(object):
    _driver_type = None
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


class HttpDriver(AbstractDriver):
    _driver_type = 'selenium'

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
        super(HttpDriver, cls)._form_desired_capabilities(driver_settings)

        if cls.loaded_dc:
            return cls.loaded_dc

        try:
            desired_capabilities = cls.capabilities_map[driver_settings["browser"].lower()]
            desired_capabilities.update(cls.loaded_settings)
        except KeyError:
            raise UnknownBrowserName(driver_settings.selenium["browser"], cls.capabilities_map.keys())

        if config.browsermobproxy['enabled']:
            cls.bmproxy.webdriver_proxy().add_to_capabilities(desired_capabilities)

        return desired_capabilities


class QtWebkitDriver(AbstractDriver):
    _driver_type = 'qtwebkitdriver'


class IosDriver(AbstractDriver):
    _driver_type = 'iosdriver'