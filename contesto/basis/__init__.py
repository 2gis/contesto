from traceback import format_exc

from contesto.core.finder import find_element
from contesto.utils import waiter
from contesto.utils.log import log


class LoadableObject(object):
    __title__ = None
    _on_load_elements = None
    _on_load_hooks = None

    def register_onload_hooks(self, hooks):
        if self._on_load_hooks is None:
            self._on_load_hooks = []

        if not isinstance(hooks, list):
            raise TypeError("Hooks must be list [], got %s instead" % type(hooks))

        self._on_load_hooks += hooks

    def register_onload_elements(self, elements):
        if self._on_load_elements is None:
            self._on_load_elements = []

        if not isinstance(elements, list):
            raise TypeError("Elements must be list [], got %s instead" % type(elements))

        self._on_load_elements += elements

    def _load(self):
        log.info("Loading %s" % self.__title__)

        if self._on_load_hooks:
            log.info("Running onload hooks")
        for hook in self._on_load_hooks:
            hook()

        if self._on_load_elements:
            log.info("Checking onload elements")
        for locator in self._on_load_elements:
            try:
                element = find_element(self.driver, locator)
                wait = waiter(element)
                wait.until(lambda el: el.is_displayed(), "Element %s is still not displayed" % el)
            except:
                raise Exception("Failed to load page: %s\n"
                                "%s\n" % (self.__title__, format_exc()))

        log.info("%s loaded" % self.__title__)

    def __init__(self, driver):
        """
        :type driver: ContestoDriver
        """
        self.driver = driver
        # backward compatibility
        self._driver = driver

        self.register_onload_elements([])
        self.register_onload_hooks([])

        if self.__title__ is None:
            self.__title__ = self.__class__.__name__

        self._load()
