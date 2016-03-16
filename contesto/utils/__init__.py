import time

from selenium.webdriver.support.wait import WebDriverWait
from werkzeug.local import LocalProxy as _Proxy

from contesto import config


class JSONSerializable:
    def to_json(self):
        res = dict()
        attrs = [name for name in vars(self) if not name.startswith('_')]
        for attr in attrs:
            res[attr] = getattr(self, attr)
        return res


class Enum(object):
    def __init__(self, *sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        self.enums = enums

    def __getattr__(self, item):
        return self.enums[item]

    def __iter__(self):
        return iter(self.enums.values())


class LocalProxy(_Proxy):
    @property
    def __class__(self):
        try:
            return type(self._get_current_object())
        except RuntimeError:
            return type(self)


class waiter(WebDriverWait):
    def __init__(self, driver, timeout=None, ignored_exceptions=None, *args, **kwargs):
        from contesto.exceptions import WebDriverException

        if timeout is None:
            timeout = float(config.timeout["normal"])

        if ignored_exceptions is None:
            ignored_exceptions = WebDriverException

        super(waiter, self).__init__(
            driver,
            timeout=timeout,
            ignored_exceptions=ignored_exceptions,
            *args, **kwargs)

    def until(self, method, message=''):
        from contesto.exceptions import TimeoutException

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions:
                pass
            time.sleep(self._poll)
            if time.time() > end_time:
                break

        raise TimeoutException(message)
