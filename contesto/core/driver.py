import re

from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from contesto import config
from contesto.core.element import ContestoWebElement
from contesto.exceptions import ElementNotFound, JavaScriptInjectionError

from ..utils.log import log


class ContestoDriver(Remote):
    def __init__(self, *args, **kwargs):
        super(ContestoDriver, self).__init__(*args, **kwargs)
        self.element_map = dict()
        self._browser = None

    def __has_to_log_command(self, driver_command):
        command_info = self.command_executor._commands.get(driver_command)
        if command_info[0] not in ["POST", "DELETE"]:
            return False
        if command_info[1].split('/')[-1] in ["session", "element", "elements"]:
            return False

        return True

    def __action_line(self, driver_command, params):
        command_info = self.command_executor._commands.get(driver_command)
        info = ""
        if "element" in command_info[1].split('/'):
            info += "[%s][%s]" % (self.element_map[params["id"]][1], params["id"])

        if driver_command.startswith("sendKeys"):
            info += " [%s]" % "".join(params['value'])

        if driver_command == "get":
            info += "[%s]" % params['url']

        line = "%-20s %s"
        if info:
            return line % (driver_command, info)
        else:
            return line % (driver_command, params)

    def execute(self, driver_command, params=None):
        def get_element_info(params):
            return params.get('using', params), params.get('value', params)

        if self.__has_to_log_command(driver_command):
            log.action(self.__action_line(driver_command, params))
        result = super(ContestoDriver, self).execute(driver_command, params)
        if isinstance(result.get("value", None), WebElement):
            self.element_map[result.get("value", None).id] = get_element_info(params)
        if isinstance(result.get("value", None), list):
            for element in result.get("value", None):
                if isinstance(element, WebElement):
                    self.element_map[element.id] = get_element_info(params)
        return result

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
            raise ElementNotFound(kwargs["value"], kwargs["by"], driver=self)

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
            raise ElementNotFound(kwargs["value"], kwargs["by"], driver=self)

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
            raise ElementNotFound(sizzle_selector, "sizzle selector", driver=self)

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
            raise ElementNotFound(sizzle_selector, "sizzle selector", driver=self)

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
