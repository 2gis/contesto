from datetime import datetime
from contesto import config


def save_screenshot_(driver, path=None, clean=False):
    """
    :type driver: WebDriver or WebElement or ContestoDriver
    """
    if config.utils['save_screenshots']:
        if clean:
            # todo clean screenshots directory
            pass
        if driver.capabilities['takesScreenshot']:
            date_time = datetime.now().strftime('%Y_%m_%d_%H_%M')
            scr_file = '%s_screenshot.png' % date_time

            if path is not None:
                scr_file = '%s%s' % (path, scr_file)
            driver.save_screenshot(scr_file)
        else:
            raise EnvironmentError('Option <takesScreenshot> in Capabilities is disabled. Please enable option for save screenshot.')
    else:
        raise EnvironmentError('Option <save_screenshots> in config is disabled. Please enable option for save screenshot.')