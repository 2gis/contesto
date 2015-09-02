import time

from selenium.webdriver.support.wait import WebDriverWait

from .log import log
from contesto import config
from contesto.utils.screenshot import make_screenshot


class Enum(object):
    def __init__(self, *sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        self.enums = enums

    def __getattr__(self, item):
        return self.enums[item]

    def __iter__(self):
        return iter(self.enums.values())


class waiter(WebDriverWait):
    def __init__(self, driver, timeout=None, ignored_exceptions=None, *args, **kwargs):
        from contesto.exceptions import WebDriverException

        if timeout is None:
            timeout = float(config.timeout["normal"])

        if ignored_exceptions is None:
            ignored_exceptions = WebDriverException

        super(waiter, self).__init__(
            driver,
            timeout=timeout,
            ignored_exceptions=ignored_exceptions,
            *args, **kwargs)

    def until(self, method, message=''):
        from contesto.exceptions import TimeoutException

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions:
                pass
            time.sleep(self._poll)
            if time.time() > end_time:
                break

        raise TimeoutException(message)


