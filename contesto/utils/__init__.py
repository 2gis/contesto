from datetime import datetime
import time

from selenium.webdriver.support.wait import WebDriverWait

from .log import log

from contesto import config


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

        # if error:
        #     log.exception(error)
        raise TimeoutException(message)


def make_screenshot(driver, path=None, clean=False):
    """
    :type driver: WebDriver or WebElement or ContestoDriver
    """
    if clean:
        # todo clean screenshots directory
        pass
    if driver.capabilities['takesScreenshot']:
        date_time = datetime.now().strftime('%Y_%m_%d_%H_%M')
        if driver.testMethodName is not None:
            scr_file = '%s_%s_screenshot.png' % (date_time, driver.testMethodName)
        else:
            scr_file = '%s_screenshot.png' % date_time

        if path is not None:
            scr_file = '%s%s' % (path, scr_file)
        driver.save_screenshot(scr_file)
    else:
        raise EnvironmentError('Option "takesScreenshot" in Capabilities is disabled.\n'
                               'Please enable option to save screenshot.')