from utils.utils import make_screenshot_
from contesto import config


class BaseError(Exception):
    pass


class ElementNotFound(BaseError):
    def __init__(self, value, by, driver=None):
        self.value, self.by, self.driver = value, by, driver

    def make_screenshot_(self):
        if config.utils['save_screenshots']:
            if self.driver is not None:
                make_screenshot_(self.driver, path='screenshots/')

    def __str__(self):
        self.make_screenshot_()
        return "Element '%s' not found by '%s'" % (self.value, self.by)


class ConnectionError(BaseError):
    def __init__(self, command_executor):
        self.command_executor = command_executor

    def __str__(self):
        return "It seems, Selenium Server is not running on %s" % self.command_executor


class JavaScriptInjectionError(BaseError):
    def __init__(self, script_name):
        self.script_name = script_name

    def __str__(self):
        return "Couldn't inject %s" % self.script_name


class UnknownBrowserName(BaseError):
    def __init__(self, browser_name, allowed_browsers):
        self.browser_name, self.allowed_browsers = browser_name, allowed_browsers

    def __str__(self):
        return "Browser name should be one of the following: " + str(self.allowed_browsers) + ", not a %s." % self.browser_name
