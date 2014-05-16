from contesto.exceptions import UnknownBrowserName

from selenium.webdriver import DesiredCapabilities


class AbstractDriver(object):
    _driver_type = None
    dc_from_config = None

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        try:
            cls.dc_from_config = driver_settings["desired_capabilities"]
        except KeyError:
            pass


class HttpDriver(AbstractDriver):
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
    _driver_type = 'selenium'

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        super(HttpDriver, cls)._form_desired_capabilities(driver_settings)
        if cls.dc_from_config:
            return cls.dc_from_config

        try:
            desired_capabilities = cls.capabilities_map[driver_settings["browser"].lower()]
        except KeyError:
            raise UnknownBrowserName(driver_settings.selenium["browser"], cls.capabilities_map.keys())

        for key, value in driver_settings.iteritems():
        ### todo IEDriver becomes insane with host/port parameters in desired_capabilities, need investigation
            if key not in ('host', 'port'):
                desired_capabilities[key] = value

        return desired_capabilities


class QtWebkitDriver(AbstractDriver):
    _driver_type = 'qtwebkitdriver'

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        super(QtWebkitDriver, cls)._form_desired_capabilities(driver_settings)
        if cls.dc_from_config:
            return cls.dc_from_config

        desired_capabilities = dict()
        desired_capabilities['app'] = driver_settings["app"]
        return desired_capabilities


class IosDriver(AbstractDriver):
    _driver_type = 'iosdriver'

    @classmethod
    def _form_desired_capabilities(cls, driver_settings):
        super(IosDriver, cls)._form_desired_capabilities(driver_settings)
        if cls.dc_from_config:
            return cls.dc_from_config

        desired_capabilities = dict()
        desired_capabilities['app'] = driver_settings["app"]
        desired_capabilities['device'] = driver_settings["device"]
        desired_capabilities['platform'] = driver_settings["platform"]
        desired_capabilities['version'] = driver_settings["version"]
        return desired_capabilities