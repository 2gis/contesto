import re

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from contesto import config
from contesto.exceptions import ElementNotFound, JavaScriptInjectionError
from ..utils.utils import save_screenshot_


class ContestoWebElement(WebElement):
    ### @todo class very similar to ContestoWebDriver (especially sizzle-part). Common parts in separate class
    def __init__(self, web_element):
        """
        :type web_element: WebElement
        """
        self.__dict__.update(web_element.__dict__)

    @property
    def text(self):
        wait = WebDriverWait(super(ContestoWebElement, self), float(config.timeout["normal"]))
        text = wait.until(lambda el: el.text)

        return text

    def js_click(self):
        self.parent.execute_script("arguments[0].click();", self)

    def find_element(self, *args, **kwargs):
        """
        :rtype: ContestoWebElement
        :raise: ElementNotFound
        """
        wait = WebDriverWait(super(ContestoWebElement, self),
                             float(config.timeout["normal"]),
                             ignored_exceptions=WebDriverException)
        try:
            element = wait.until(lambda el: el.find_element(*args, **kwargs))
        except TimeoutException:
            save_screenshot_(driver=self, path='screenshots/')
            raise ElementNotFound(kwargs["value"], kwargs["by"])

        return ContestoWebElement(element)

    def find_elements(self, *args, **kwargs):
        """
        :rtype: list of ContestoWebElement
        :raise: ElementNotFound
        """
        wait = WebDriverWait(super(ContestoWebElement, self),
                             float(config.timeout["normal"]),
                             ignored_exceptions=WebDriverException)
        try:
            elements = wait.until(lambda el: el.find_elements(*args, **kwargs))
        except TimeoutException:
            save_screenshot_(driver=self, path='screenshots/')
            raise ElementNotFound(kwargs["value"], kwargs["by"])

        return [ContestoWebElement(element) for element in elements]

    def find_element_by_sizzle(self, sizzle_selector):
        """
        :type sizzle_selector: str
        :rtype: ContestoWebElement
        :raise: ElementNotFound
        """
        if not self._is_sizzle_loaded():
            self._inject_sizzle()

        wait = WebDriverWait(self, float(config.timeout["normal"]))
        try:
            elements = wait.until(lambda el: el.parent.execute_script(el._make_sizzle_string(sizzle_selector), el))
        except TimeoutException:
            save_screenshot_(driver=self, path='screenshots/')
            raise ElementNotFound(sizzle_selector, "sizzle selector")

        return ContestoWebElement(elements[0])

    def find_elements_by_sizzle(self, sizzle_selector):
        """
        :type sizzle_selector: str
        :rtype: list of ContestoWebElement
        :raise: ElementNotFound
        """
        if not self._is_sizzle_loaded():
            self._inject_sizzle()

        wait = WebDriverWait(self, float(config.timeout["normal"]))
        try:
            elements = wait.until(lambda el: el.parent.execute_script(el._make_sizzle_string(sizzle_selector), el))
        except TimeoutException:
            save_screenshot_(driver=self, path='screenshots/')
            raise ElementNotFound(sizzle_selector, "sizzle selector")

        return [ContestoWebElement(element) for element in elements]

    def _inject_sizzle(self):
        """
        :raise: JavaScriptInjectionError
        """
        ### @todo http/https
        ### @todo static file
        script = """
            var _s = document.createElement("script");
            _s.type = "text/javascript";
            _s.src = "%s";
            var _h = document.getElementsByTagName('head')[0];
            _h.appendChild(_s);
        """ % config.sizzle["url"]
        self.parent.execute_script(script)
        wait = WebDriverWait(self, float(config.timeout["normal"]))
        try:
            wait.until(lambda el: el._is_sizzle_loaded())
        except TimeoutException:
            save_screenshot_(driver=self, path='screenshots/')
            raise JavaScriptInjectionError("Sizzle")

    def _is_sizzle_loaded(self):
        """
        :rtype: bool
        """
        script = "return typeof(Sizzle) != \"undefined\";"

        return self.parent.execute_script(script)

    @staticmethod
    def _make_sizzle_string(sizzle_selector):
        """
        :rtype: str
        """
        if isinstance(sizzle_selector, str):
            sizzle_selector = sizzle_selector.decode("utf-8")

        return "return Sizzle(\"%s\", arguments[0]);" % re.escape(sizzle_selector)
