# coding: utf-8
from datetime import datetime
from functools import wraps
import re

from contesto import config
from contesto.utils import log


def make_screenshot(driver, path=None, clean=False):
    """
    :type driver: WebDriver or WebElement or ContestoDriver
    """
    if clean:
        # todo clean screenshots directory
        pass
    if driver.capabilities['takesScreenshot']:
        date_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
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


def _try_make_screenshot(obj):
    if config.utils.get('save_screenshots'):
        path = config.utils.get('screenshots_path', 'screenshots/')
        driver = getattr(obj, 'driver', None)
        if driver is None:
            return
        path = path.rstrip('/') + '/'
        try:
            make_screenshot(driver, path)
        except Exception as e:
            log.warning("Unexpected exception %s occurred while trying to save screenshot", e)


def save_screenshot_on_error(func):
    """
    Saves screenshot if method raised exception and `save_screenshots` option in `utils` section is set.
    Screenshot is saved to `screenshots_path` defined in `utils` section of config.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            _try_make_screenshot(self)
            raise

    return wrapper


class SaveScreenshotOnError(type):
    """
    A metaclass that decorates all methods matching `__save_screenshot_pattern__` with :func:`save_screenshot_on_error`
    """
    DEFAULT_PATTERN = '(?:^|[\\b_\\.-])[Tt]est'

    def __new__(mcs, name, bases, local):
        pattern = local.get('__save_screenshot_pattern__', mcs.DEFAULT_PATTERN)
        regex = re.compile(pattern)
        for attr in local:
            if regex.match(attr):
                value = local[attr]
                if callable(value):
                    local[attr] = save_screenshot_on_error(value)
        return type.__new__(mcs, name, bases, local)
