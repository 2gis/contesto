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

from contesto import config
from contesto.core.driver import Driver
from contesto.utils.screenshot import save_screenshot_on_error, SaveScreenshotOnError


@nottest
def fixture_driver():
    class MyDriver(Driver):
        def __init__(self):
            super(MyDriver, self).__init__()
            self.capabilities = {'takesScreenshot': True}
            self.save_screenshot = Mock()

    return MyDriver()


@nottest
def fixture_simple_test_case():
    class MyTestCase(unittest.TestCase):
        driver = fixture_driver()

        def runTest(self):
            raise ValueError('123')

    return MyTestCase


@nottest
def fixture_test_case():
    class MyTestCase(unittest.TestCase):
        driver = fixture_driver()

        def test_method1(self):
            raise ValueError('123')

        def test_method2(self):
            raise ValueError('123')

        def test_method3(self):
            pass

        def some_helper(self):
            pass

    return MyTestCase


class SaveScreenshotOnErrorDecoratorTest(unittest.TestCase):
    def setUp(self):
        config.utils = {'save_screenshots': ''}
        test_case_cls = fixture_simple_test_case()
        test_case_cls.runTest = save_screenshot_on_error(test_case_cls.runTest)
        self.test_case = test_case_cls()

    def test_should_save_screenshot(self):
        config.utils['save_screenshots'] = True
        with self.assertRaises(ValueError):
            self.test_case.runTest()
        self.assertEqual(1, self.test_case.driver.save_screenshot.call_count)

    def test_should_not_save_screenshot_if_not_save_screenshots(self):
        config.utils['save_screenshots'] = False
        with self.assertRaises(ValueError):
            self.test_case.runTest()

        self.test_case.driver.save_screenshot.assert_not_called()

    def test_should_save_screenshot_using_specified_path(self):
        config.utils['save_screenshots'] = True
        config.utils['screenshots_path'] = '/some/test/path'
        with self.assertRaises(ValueError):
            self.test_case.runTest()

        self.assertEqual(1, self.test_case.driver.save_screenshot.call_count)
        self.test_case.driver.save_screenshot.call_args[0][0].startswith('/some/test/path')

    def test_should_not_save_screenshot_if_driver_is_none(self):
        config.utils['save_screenshots'] = True
        self.test_case.driver = None
        with patch('contesto.utils.screenshot.make_screenshot') as mock:
            with self.assertRaises(ValueError):
                self.test_case.runTest()
        self.assertFalse(mock.called)


class DecoratorUnittestIntegrationTest(unittest.TestCase):
    def setUp(self):
        config.utils['save_screenshots'] = True

    def test_decorator(self):
        test_case_cls = fixture_test_case()
        test_case_cls.test_method1 = save_screenshot_on_error(test_case_cls.test_method1)
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        result = runner.run(unittest.TestSuite(map(test_case_cls, ['test_method1'])))

        self.assertEqual(1, test_case_cls.driver.save_screenshot.call_count)
        self.assertEqual(1, len(result.errors))


class MetaclassUnittestIntegrationTest(unittest.TestCase):
    def setUp(self):
        config.utils['save_screenshots'] = True
        self.test_case_cls = fixture_test_case()

    def apply_metaclass_and_run(self):
        self.test_case_cls = SaveScreenshotOnError(self.test_case_cls.__name__,
                                                   self.test_case_cls.__bases__,
                                                   self.test_case_cls.__dict__.copy())
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        self.result = runner.run(unittest.makeSuite(self.test_case_cls))

    def test_metaclass(self):
        self.apply_metaclass_and_run()

        self.assertEqual(3, self.result.testsRun)
        self.assertEqual(2, self.test_case_cls.driver.save_screenshot.call_count)
        self.assertEqual(2, len(self.result.errors))

    def test_metaclass_with_pattern(self):
        self.test_case_cls.__save_screenshot_pattern__ = 'test_method1'
        self.apply_metaclass_and_run()

        self.assertEqual(3, self.result.testsRun)
        self.assertEqual(1, self.test_case_cls.driver.save_screenshot.call_count)
        self.assertEqual(2, len(self.result.errors))
