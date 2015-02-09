import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from contesto import config
from contesto.utils.log import log


class waiter(WebDriverWait):
    def __init__(self, driver, timeout=None, ignored_exceptions=None, *args, **kwargs):
        if timeout is None:
            timeout=float(config.timeout["normal"])

        if ignored_exceptions is None:
            ignored_exceptions=WebDriverException

        super(waiter, self).__init__(
            driver,
            timeout=timeout,
            ignored_exceptions=ignored_exceptions,
            *args, **kwargs)

    def until(self, method, message=''):
        end_time = time.time() + self._timeout
        error = None
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions as e:
                error = e
            time.sleep(self._poll)
            if time.time() > end_time:
                break

        if error:
            log.exception(error)
        raise TimeoutException(message)