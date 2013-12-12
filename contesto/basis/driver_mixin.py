from contesto.exceptions import UnknownBrowserName


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
        desired_capabilities["platform"] = driver_settings["platform"]
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
