from config import config

from .basis.test_case import ContestoTestCase, \
    UnittestContestoTestCase, PyTestContestoTestCase  # deprecated
from .core.locator import Locator
from .core.finder import find_element, find_elements
from .basis.page import Page
from .basis.component import MobileComponent, BaseComponent
from .basis.driver_mixin import SeleniumDriverMixin,\
    QtWebkitDriverMixin, IosDriverMixin, AndroidDriverMixin
