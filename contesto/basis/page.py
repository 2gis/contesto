from traceback import format_exc

from selenium.webdriver import TouchActions

from contesto.utils.log import log
from contesto import find_element
from contesto.utils import waiter


class Page(object):
    """
    Base class for Page. The main of Page is encapsulate page elements
    for mobile, web or desktop application.
    """

    title = None
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

    def _page_on_load(self):
        log.info("Loading page %s" % self.title)

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
                wait.until(lambda el: el.is_displayed())
            except:
                raise Exception("Failed to load page: %s\n"
                                "%s\n" % (self.title, format_exc()))

        log.info("%s loaded" % self.title)

    def __init__(self, driver):
        """
        :type driver: ContestoDriver
        """
        self.driver = driver
        # backward compatibility
        self._driver = driver

        self.register_onload_elements([])
        self.register_onload_hooks([])

        if self.title is None:
            self.title = self.__class__.__name__

        self._page_on_load()

    def get_source(self):
        return self.driver.page_source


class WebPage(Page):
    @property
    def url(self):
        return self.driver.current_url

    def get(self, url):
        """
        :type url: str
        """
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()


class IosScreen(Page):
    def scroll_page(self, x, y):
        TouchActions(self.driver).flick(x, y).perform()


BasePage = WebPage

