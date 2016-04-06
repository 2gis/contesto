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
from contesto.utils.error_handler import collect_on_error


@nottest
def test_case_with_collect_metadata_on_error_decorator():
    class MyTestCase(ContestoTestCase):
        driver = Mock()

        @staticmethod
        def _create_session(*args, **kwargs):
            return Mock()

        @collect_on_error
        def test_method(self):
            raise ValueError('123')

    return MyTestCase('test_method')


@nottest
def fixture_test_case():
    class MyTestCaseWithScreenshot(ContestoTestCase):
        def test_method(self):
            raise ValueError('123')

    return MyTestCaseWithScreenshot('test_method')


@nottest
def test_case_will_fail():
    class TestWithFailOnSetupTest(ContestoTestCase):
        def _setup_test(self):
            raise ValueError('123')

        def test_method(self):
            pass

    return TestWithFailOnSetupTest('test_method')


class TestCaseFailedDuringSetUp(unittest.TestCase):
    def setUp(self):
        self._config_collect_metadata = config.utils["collect_metadata"]

    def tearDown(self):
        config.utils["collect_metadata"] = self._config_collect_metadata

    def test_should_collect_metadata_when_fails_on_setup(self):
        config.utils['collect_metadata'] = True
        test_case = test_case_will_fail()
        test_case._init_context()
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            test_case.run()
        self.assertEqual(1, m.call_count)


class ContestoTestCaseCollectMetadata(unittest.TestCase):
    def setUp(self):
        self._config_collect_metadata = config.utils["collect_metadata"]

    def tearDown(self):
        config.utils["collect_metadata"] = self._config_collect_metadata

    def test_should_collect_metadata(self):
        config.utils['collect_metadata'] = True
        test_case = fixture_test_case()
        test_case._init_context()
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            test_case.run()
        self.assertEqual(1, m.call_count)

    def test_should_not_collect_metadata_if_not_collect_metadata(self):
        config.utils['collect_metadata'] = False
        test_case = fixture_test_case()
        test_case._init_context()
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            with self.assertRaises(ValueError):
                test_case.test_method()
        self.assertEqual(0, m.call_count)

    def test_should_not_save_screenshot_if_screenshot_is_none(self):
        config.utils['collect_metadata'] = True
        self.test_case = fixture_test_case()
        self.test_case._init_context()
        self.test_case.screenshot = None
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            self.test_case.run()
        self.assertTrue(m.called)


class DecoratedTestCollectMetadataOnError(unittest.TestCase):
    def test_decorator(self):
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            test_case = test_case_with_collect_metadata_on_error_decorator()
            stream = StringIO()
            runner = unittest.TextTestRunner(stream=stream)
            result = runner.run(unittest.TestSuite([test_case]))
        self.assertEqual(1, m.call_count)
        self.assertEqual(1, len(result.errors))


class TestReportMetadataToFile(unittest.TestCase):
    def setUp(self):
        self._config_collect_metadata = config.utils["collect_metadata"]

    def tearDown(self):
        config.utils["collect_metadata"] = self._config_collect_metadata

    def test_should_collect_using_specified_path(self):
        config.utils['collect_metadata'] = True
        config.utils['metadata_path'] = '/some/test/path'
        self.test_case = fixture_test_case()
        self.test_case._init_context()
        with patch('contesto.utils.error_handler.report_to_file', Mock()) as m:
            self.test_case.run()

        self.assertEqual(1, m.call_count)
        self.assertTrue(m.call_args[0][0].startswith('/some/test/path'))

