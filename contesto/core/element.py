import re

from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from appium.webdriver.webelement import WebElement as AppiumWebElement

from contesto import config
from contesto.exceptions import ElementNotFound, JavaScriptInjectionError, ElementIsNotClickable, \
    ContestoDriverException, ElementNotVisibleException


class ContestoWebElement(SeleniumWebElement):
    def js_click(self):
        try:
            self.parent.execute_script("arguments[0].click();", self)
        except WebDriverException as e:
            raise ContestoDriverException(e.msg, e.screen, e.stacktrace, driver=self.parent)

    def click(self):
        """
        :raise: ElementNotFound
        """
        try:
            super(ContestoWebElement, self).click()
        except WebDriverException as e:
            raise ElementIsNotClickable(e.msg, e.screen, e.stacktrace, driver=self.parent)

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
            raise ElementNotFound(sizzle_selector, "sizzle selector", driver=self.parent)

        return elements[0]

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
            raise ElementNotFound(sizzle_selector, "sizzle selector", driver=self.parent)

        return elements

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


class ContestoMobileElement(AppiumWebElement):
    pass