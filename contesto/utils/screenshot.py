# coding: utf-8
import os
from datetime import datetime

from contesto import config
from contesto.globals import current_test
from contesto.utils.log import log


def _make_screenshot(driver, path, clean=False):
    """
    Saves screenshot of the current window in ``path`` folder with file name combined of current test name and date.

    :type driver: WebDriver or WebElement or ContestoDriver
    """
    if clean:
        # todo clean screenshots directory
        pass
    if driver.capabilities['takesScreenshot']:
        date_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        fname = '%s%s.png' % (str(current_test), date_time)
        scr_file = os.path.sep.join([path, fname])

        if driver.save_screenshot(scr_file):
            current_test._meta_info['attachments'].append(
                {
                    'path': scr_file,
                    'mime_type': 'image/png',
                    'name': 'screenshot'
                }
            )
        else:
            log.warn("Could not save screenshot for %s" % str(current_test))
    else:
        raise EnvironmentError(
            'Option "takesScreenshot" in Capabilities is disabled.\n'
            'Please enable option to save screenshot.')


def _try_make_screenshot():
    path = config.utils.get('screenshots_path', None)
    if path is None:
        log.info("No 'screenshot_path' provided in config. Defaulting to 'screenshots'")
        path = 'screenshots'

    driver = getattr(current_test, 'driver', None)
    if driver is None:
        log.info("%s has no driver object. Aborting taking error screenshot." % str(current_test))
        return
    path = path.rstrip(os.path.sep)
    try:
        _make_screenshot(driver, path)
    except Exception as e:
        log.warning("Unexpected exception %s occurred while trying to save screenshot", e)
