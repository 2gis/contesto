# coding: utf-8

from .element import ContestoWebElement

from ..exceptions import TimeoutException, ElementNotFound
from ..utils import waiter
from ..utils.log import log


def find_element(obj, locator):
    wait = waiter(obj)
    log.internal(u"Trying to find element: %s, timeout: %s" % (locator, wait._timeout))
    try:
        element = wait.until(lambda dr: dr.find_element(by=locator["by"], value=locator["value"]))
    except TimeoutException as e:
        log.exception(e)
        raise ElementNotFound(locator["value"], locator["by"])

    return ContestoWebElement(element)


def find_elements(obj, locator):
    wait = waiter(obj)
    log.internal(u"Trying to find elements: %s, timeout: %s" % (locator, wait._timeout))
    try:
        elements = wait.until(lambda dr: dr.find_elements(by=locator["by"], value=locator["value"]))
    except TimeoutException as e:
        log.exception(e)
        raise ElementNotFound(locator["value"], locator["by"])

    return [ContestoWebElement(element) for element in elements]