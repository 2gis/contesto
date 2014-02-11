from contesto.utils.extending import AutoExtendingSelectors
from contesto.utils.log import trace


class BaseComponent(object):
    __metaclass__ = AutoExtendingSelectors

    def __init__(self, driver, element=None):
        """
        :type driver: ContestoDriver
        :type element: ContestoWebElement
        """
        self.driver = driver
        self.element = element
        trace(self.__class__)
