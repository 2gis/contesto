from selenium.webdriver import TouchActions
from contesto.basis import LoadableObject


class Page(LoadableObject):
    """
    Base class for Page. The main of Page is encapsulate page elements
    for mobile, web or desktop application.
    """

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

