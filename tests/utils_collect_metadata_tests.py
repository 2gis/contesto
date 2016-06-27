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


@nottest
def fixture_test_case():
    class MyTestCaseWithScreenshot(ContestoTestCase):
        driver = Mock(page_source=Mock())

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


class TestCaseUsingConfig(unittest.TestCase):
    def setUp(self):
        self._config_collect_metadata = config.utils["collect_metadata"]

    def tearDown(self):
        config.utils["collect_metadata"] = self._config_collect_metadata
        config.utils['collect_page_source'] = True


class ContestoTestCaseCollectMetadata(TestCaseUsingConfig):
    def test_should_collect_metadata(self):
        config.utils['collect_metadata'] = True
        test_case = fixture_test_case()
        test_case.run()
        self.assertIn('stack_trace', test_case._meta_info.keys())
        self.assertIn('message', test_case._meta_info.keys())
        attachments = [
            item["name"] for item in test_case._meta_info['attachments']
        ]
        self.assertIn("page_source", attachments)

    def test_should_not_collect_metadata_if_not_collect_metadata(self):
        config.utils['collect_metadata'] = False
        test_case = fixture_test_case()
        test_case.run()
        self.assertNotIn('stack_trace', test_case._meta_info.keys())
        self.assertNotIn('message', test_case._meta_info.keys())
        self.assertListEqual([], test_case._meta_info['attachments'])

    def test_should_collect_metadata_when_fails_on_setup(self):
        config.utils['collect_metadata'] = True
        test_case = test_case_will_fail()
        test_case.run()
        self.assertIn('stack_trace', test_case._meta_info.keys())
        self.assertIn('message', test_case._meta_info.keys())
        self.assertIn('attachments', test_case._meta_info.keys())
        self.assertListEqual([], test_case._meta_info['attachments'])

    def test_should_collect_using_specified_path(self):
        config.utils['collect_metadata'] = True
        config.utils['metadata_path'] = '/some/test/path'
        test_case = fixture_test_case()
        with patch('contesto.utils.collect.report_to_file') as m:
            test_case.run()
        self.assertTrue(m.called)
        self.assertTrue(m.call_args[0][0].startswith('/some/test/path'))

    def test_disable_page_source_collecting(self):
        config.utils['collect_metadata'] = True
        config.utils['collect_page_source'] = False
        test_case = fixture_test_case()
        test_case.run()
        self.assertIn('stack_trace', test_case._meta_info.keys())
        self.assertIn('message', test_case._meta_info.keys())
        self.assertIn('attachments', test_case._meta_info.keys())
        attachments = [
            item["name"] for item in test_case._meta_info['attachments']
        ]
        self.assertNotIn("page_source", attachments)
