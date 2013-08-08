import re

from selenium.webdriver import Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from contesto import config
from contesto.core.element import ContestoWebElement
from contesto.exceptions import ElementNotFound, JavaScriptInjectionError


class ContestoDriver(Remote):
    def __init__(self, *args, **kwargs):
        super(ContestoDriver, self).__init__(*args, **kwargs)
        self._browser = None

    @property
    def browser(self):
        """
        :rtype: str
        """
        if self._browser is None:
            self._browser = self.capabilities['browserName']

        return self._browser

    def find_element(self, *args, **kwargs):
        """
        :rtype: ContestoWebElement
        :raise: ElementNotFound
        """
        wait = WebDriverWait(super(ContestoDriver, self),
                             float(config.timeout["normal"]),
                             ignored_exceptions=WebDriverException)
        try:
            element = wait.until(lambda dr: dr.find_element(*args, **kwargs))
        except TimeoutException:
            raise ElementNotFound(kwargs["value"], kwargs["by"])

        return ContestoWebElement(element)

    def find_elements(self, *args, **kwargs):
        """
        :rtype: list of ContestoWebElement
        :raise: ElementNotFound
        """
        wait = WebDriverWait(super(ContestoDriver, self),
                             float(config.timeout["normal"]),
                             ignored_exceptions=WebDriverException)
        try:
            elements = wait.until(lambda dr: dr.find_elements(*args, **kwargs))
        except TimeoutException:
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
            elements = wait.until(lambda dr: dr.execute_script(dr._make_sizzle_string(sizzle_selector)))
        except TimeoutException:
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
            elements = wait.until(lambda dr: dr.execute_script(dr._make_sizzle_string(sizzle_selector)))
        except TimeoutException:
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
        self.execute_script(script)
        wait = WebDriverWait(self, float(config.timeout["normal"]))
        try:
            wait.until(lambda dr: dr._is_sizzle_loaded())
        except TimeoutException:
            raise JavaScriptInjectionError("Sizzle")

    def _is_sizzle_loaded(self):
        """
        :rtype: bool
        """
        script = "return typeof(Sizzle) != \"undefined\";"

        return self.execute_script(script)

    @staticmethod
    def _make_sizzle_string(sizzle_selector):
        """
        :rtype: str
        """
        if isinstance(sizzle_selector, str):
            sizzle_selector = sizzle_selector.decode("utf-8")

        return "return Sizzle(\"%s\");" % re.escape(sizzle_selector)
