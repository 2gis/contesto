import re

from selenium.webdriver import Remote as SeleniumDriver
from appium.webdriver import Remote as AppiumDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

from contesto.core.element import ContestoWebElement, ContestoMobileElement
from contesto.exceptions import ElementNotFound, JavaScriptInjectionError, PageCantBeLoadedException
from contesto.utils.log import log

from contesto import config


class Driver(object):
    def __init__(self, *args, **kwargs):
        super(Driver, self).__init__(*args, **kwargs)
        self.element_map = dict()
        self._browser = None
        self._testMethodName = None

    def __has_to_log_command(self, driver_command):
        command_info = self.command_executor._commands.get(driver_command)
        if command_info[0] not in ["POST", "DELETE"]:
            return False
        if command_info[1].split('/')[-1] in ["session", "element", "elements", "push_file"]:
            return False

        return True

    def __action_line(self, driver_command, params):
        command_info = self.command_executor._commands.get(driver_command)
        info = ""
        if ("element" and not 'active') in command_info[1].split('/'):
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
            if params is not None:
                return params.get('using', params), params.get('value', params)

        if self.__has_to_log_command(driver_command):
            log.debug(self.__action_line(driver_command, params))
        result = super(Driver, self).execute(driver_command, params)
        if isinstance(result.get("value", None), WebElement):
            self.element_map[result.get("value", None).id] = get_element_info(params)
        if isinstance(result.get("value", None), list):
            for element in result.get("value", None):
                if isinstance(element, WebElement):
                    self.element_map[element.id] = get_element_info(params)
        return result

    @property
    def testMethodName(self):
        """
        :rtype: str
        """
        if self._testMethodName is not None:
            return self._testMethodName.split('(')[0]


class ContestoWebDriver(Driver, SeleniumDriver):
    @property
    def browser(self):
        """
        :rtype: str
        """
        if self._browser is None:
            self._browser = self.capabilities['browserName']

        return self._browser

    def get(self, url):
        wait = WebDriverWait(super(ContestoWebDriver, self),
                             float(config.timeout["normal"]),
                             ignored_exceptions=WebDriverException)
        try:
            super(ContestoWebDriver, self).get(url)
            wait.until(lambda dr: self.page_loaded())
        except TimeoutException as e:
            raise PageCantBeLoadedException("Page can not be loaded with url: %s" % url, e.screen, e.stacktrace, driver=self)

    def page_loaded(self):
        pl = self.execute_script('return document.readyState;')

        log.info("Status Page Loaded: %s" % pl)
        return pl == 'complete'

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
            elements = wait.until(lambda dr: dr.execute_script(dr._make_sizzle_string(sizzle_selector)))
        except TimeoutException:
            raise ElementNotFound(sizzle_selector, "sizzle selector", driver=self)

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

    def create_web_element(self, element_id):
        return ContestoWebElement(self, element_id, self.w3c)


class ContestoMobileDriver(Driver, AppiumDriver):
    def create_web_element(self, element_id):
        return ContestoMobileElement(self, element_id, self.w3c)
