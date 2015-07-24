from config import config

from .basis.test_case import ContestoTestCase, \
    UnittestContestoTestCase, PyTestContestoTestCase  # deprecated
from .core.locator import *
from .core.finder import find_element, find_elements
from .basis.page import Page, WebPage, MobilePage
from .basis.component import Component, WebComponent, MobileComponent
from .basis.driver_mixin import *
