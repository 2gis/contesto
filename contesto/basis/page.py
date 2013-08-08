class BasePage(object):
    def __init__(self, driver):
        """
        :type driver: ContestoDriver
        """
        self._driver = driver

    def get(self, url):
        """
        :type url: str
        """
        self._driver.get(url)

    def forward(self):
        self._driver.forward()

    def back(self):
        self._driver.back()
