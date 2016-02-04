# coding: utf-8
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

from nose.tools import nottest

from contesto import ContestoTestCase, config
from contesto.core.driver import Driver
from contesto.utils.screenshot import save_screenshot_on_error


@nottest
def mock_driver():
    class MyDriver(Driver):
        def __init__(self):
            super(MyDriver, self).__init__()
            self.capabilities = {'takesScreenshot': True}
            self.save_screenshot = Mock()

    return MyDriver()


@nottest
def test_case_with_save_screenshot_on_error_decorator():
    class MyTestCase(unittest.TestCase):
        driver = mock_driver()

        @save_screenshot_on_error
        def test_method(self):
            raise ValueError('123')

    return MyTestCase('test_method')


@nottest
def fixture_test_case():
    class MyTestCase(ContestoTestCase):
        driver = mock_driver()

        def test_method(self):
            raise ValueError('123')

    return MyTestCase('test_method')


class ContestoTestCaseSavesScreenshotOnError(unittest.TestCase):
    def test_should_save_screenshot(self):
        config.utils['save_screenshots'] = True
        test_case = fixture_test_case()
        with self.assertRaises(ValueError):
            test_case.test_method()
        self.assertEqual(1, test_case.driver.save_screenshot.call_count)

    def test_should_not_save_screenshot_if_not_save_screenshots(self):
        config.utils['save_screenshots'] = False
        test_case = fixture_test_case()
        with self.assertRaises(ValueError):
            test_case.test_method()

        test_case.driver.save_screenshot.assert_not_called()


class DecoratedTestSavesScreenshotOnError(unittest.TestCase):
    def test_decorator(self):
        test_case = test_case_with_save_screenshot_on_error_decorator()
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        result = runner.run(unittest.TestSuite([test_case]))
        self.assertEqual(1, test_case.driver.save_screenshot.call_count)
        self.assertEqual(1, len(result.errors))


class TestScreenshotSaving(unittest.TestCase):
    def setUp(self):
        self.test_case = fixture_test_case()

    def test_should_save_screenshot_using_specified_path(self):
        config.utils['save_screenshots'] = True
        config.utils['screenshots_path'] = '/some/test/path'
        with self.assertRaises(ValueError):
            self.test_case.test_method()

        self.assertEqual(1, self.test_case.driver.save_screenshot.call_count)
        self.test_case.driver.save_screenshot.call_args[0][0].startswith('/some/test/path')

    def test_should_not_save_screenshot_if_driver_is_none(self):
        config.utils['save_screenshots'] = True
        self.test_case.driver = None
        with patch('contesto.utils.screenshot._make_screenshot') as mock:
            with self.assertRaises(ValueError):
                self.test_case.test_method()
        self.assertFalse(mock.called)
