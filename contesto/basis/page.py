from selenium.webdriver import TouchActions
from contesto.basis import LoadableObject


class Page(LoadableObject):
    """
    The main point of Page is encapsulate page elements
    for mobile, web or desktop application.
    """

    def get_source(self):
        return self.driver.page_source


class WebPage(Page):
    """
    The main point of Page is encapsulate page elements
    for mobile, web or desktop application.
    """

    @property
    def url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()


class MobilePage(Page):
    def scroll_page(self, x, y):
        TouchActions(self.driver).flick(x, y).perform()



# backward compatibility
IosScreen = MobilePage
BasePage = WebPage
