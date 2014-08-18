from selenium.webdriver import TouchActions


class Page(object):
    """
    Base class for Page. The main of Page is encapsulate page elements
    for mobile, web or desktop application.
    """

    def __init__(self, driver):
        """
        :type driver: ContestoDriver
        """
        self._driver = driver

    def get_source(self):
        return self._driver.page_source


class WebPage(Page):

    @property
    def url(self):
        return self._driver.current_url

    def get(self, url):
        """
        :type url: str
        """
        self._driver.get(url)

    def refresh(self):
        self._driver.refresh()

    def forward(self):
        self._driver.forward()

    def back(self):
        self._driver.back()


class IosScreen(Page):

    def scroll_page(self, x, y):
        TouchActions(self._driver).flick(x, y).perform()

BasePage = WebPage

