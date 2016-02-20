# coding: utf-8
from contesto.exceptions import ElementNotFound, TimeoutException
from contesto.utils import waiter
from contesto.utils.log import log


def find_element(obj, locator, timeout=None):
    wait = waiter(obj, timeout=timeout)
    log.debug(u"Trying to find element: %s, timeout: %s" % (locator, wait._timeout))
    try:
        return wait.until(lambda dr: dr.find_element(by=locator["by"], value=locator["value"]))
    except TimeoutException as e:
        raise ElementNotFound(locator["value"], locator["by"])


def find_elements(obj, locator, timeout=None):
    wait = waiter(obj, timeout=timeout)
    log.debug(u"Trying to find elements: %s, timeout: %s" % (locator, wait._timeout))
    try:
        return wait.until(lambda dr: dr.find_elements(by=locator["by"], value=locator["value"]))
    except TimeoutException as e:
        raise ElementNotFound(locator["value"], locator["by"])
