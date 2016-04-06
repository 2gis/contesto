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


@nottest
def mock_driver():
    class MyDriver(Driver):
        def __init__(self):
            super(MyDriver, self).__init__()
            self.capabilities = {'takesScreenshot': True}
            self.save_screenshot = Mock()

    return MyDriver()


@nottest
def fixture_test_case():
    class MyTestCase(ContestoTestCase):
        driver = mock_driver()

        def test_method(self):
            raise ValueError('123')

    return MyTestCase('test_method')


class TestCaseUsingConfig(unittest.TestCase):
    def setUp(self):
        self._save_screenshot_default_value = config.utils['save_screenshots']

    def tearDown(self):
        config.utils['save_screenshots'] = self._save_screenshot_default_value


class ContestoTestCaseSavesScreenshotOnError(TestCaseUsingConfig):
    def test_should_save_screenshot(self):
        config.utils['save_screenshots'] = True
        test_case = fixture_test_case()
        test_case.run()
        self.assertEqual(1, test_case.driver.save_screenshot.call_count)

    def test_should_not_save_screenshot_if_not_save_screenshots(self):
        config.utils['save_screenshots'] = False
        test_case = fixture_test_case()
        test_case.run()
        test_case.driver.save_screenshot.assert_not_called()


class TestScreenshotSaving(TestCaseUsingConfig):
    def test_should_save_screenshot_using_specified_path(self):
        config.utils['save_screenshots'] = True
        config.utils['screenshots_path'] = '/some/test/path'
        test_case = fixture_test_case()
        test_case.run()
        self.assertEqual(1, test_case.driver.save_screenshot.call_count)
        test_case.driver.save_screenshot.call_args[0][0].startswith('/some/test/path')

    def test_should_not_save_screenshot_if_driver_is_none(self):
        config.utils['save_screenshots'] = True
        test_case = fixture_test_case()
        test_case.driver = None
        with patch('contesto.utils.screenshot._make_screenshot') as mock:
            test_case.run()
        self.assertFalse(mock.called)
