from utils.utils import make_screenshot_
from contesto import config
from selenium.common.exceptions import WebDriverException


class BaseError(Exception):
    pass


class ElementNotFound(BaseError):
    def __init__(self, value, by, driver=None):
        self.value, self.by, self.driver = value, by, driver

    def __str__(self):
        if config.utils['save_screenshots']:
            if self.driver is not None:
                make_screenshot_(self.driver, path='screenshots/')
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


class ContestoDriverException(WebDriverException):
    def __init__(self, msg=None, screen=None, stacktrace=None, driver=None):
        self.driver = driver
        super(ContestoDriverException, self).__init__(msg, screen, stacktrace)

    def __str__(self):
        if config.utils['save_screenshots']:
            if self.driver is not None:
                make_screenshot_(self.driver, path='screenshots/')
        exception_msg = "%s" % repr(self.msg)
        return exception_msg


class ElementIsNotClickable(ContestoDriverException):
    def __init__(self, msg=None, screen=None, stacktrace=None, driver=None):
        def make_readable_error(msg):
            for part in msg.split(":"):
                if part.find("Element is not clickable") >= 0:
                    return str(part.strip())

        super(ElementIsNotClickable, self).__init__(make_readable_error(msg), screen, stacktrace, driver)


class ErrorInResponseException(ContestoDriverException):
    def __init__(self, response, msg):
        ContestoDriverException.__init__(self, msg)
        self.response = response


class InvalidSwitchToTargetException(ContestoDriverException):
    pass


class NoSuchFrameException(InvalidSwitchToTargetException):

    pass


class NoSuchWindowException(InvalidSwitchToTargetException):

    pass


class NoSuchElementException(ContestoDriverException):
    pass


class NoSuchAttributeException(ContestoDriverException):
    pass


class StaleElementReferenceException(ContestoDriverException):
    pass


class InvalidElementStateException(ContestoDriverException):
    pass


class UnexpectedAlertPresentException(ContestoDriverException):
    def __init__(self, msg=None, screen=None, stacktrace=None, alert_text=None):
        super(ContestoDriverException, self).__init__(msg, screen, stacktrace)
        self.alert_text = alert_text

    def __str__(self):
        return "Alert Text: %s\n%s" % (self.alert_text, str(super(ContestoDriverException, self)))


class NoAlertPresentException(ContestoDriverException):
    pass


class ElementNotVisibleException(InvalidElementStateException):
    pass


class ElementNotSelectableException(InvalidElementStateException):
    pass


class InvalidCookieDomainException(ContestoDriverException):
    pass


class UnableToSetCookieException(ContestoDriverException):
    pass


class RemoteDriverServerException(ContestoDriverException):
    pass


class TimeoutException(ContestoDriverException):

    pass


class MoveTargetOutOfBoundsException(ContestoDriverException):
    pass


class UnexpectedTagNameException(ContestoDriverException):
    pass


class InvalidSelectorException(NoSuchElementException):

    pass


class ImeNotAvailableException(ContestoDriverException):

    pass


class ImeActivationFailedException(ContestoDriverException):
    pass