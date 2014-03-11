class BaseError(Exception):
    pass


class ElementNotFound(BaseError):
    def __init__(self, value, by):
        self.value, self.by = value, by

    def __str__(self):
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
