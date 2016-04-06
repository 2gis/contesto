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
from contesto import ContestoTestCase


@nottest
def test_case_ok():
    class MyTestCaseOk(ContestoTestCase):
        driver = Mock()

        @classmethod
        def _setup_class(cls):
            pass

        def _setup_test(*args, **kwargs):
            pass

        def test_method(self):
            pass

        def _teardown_test(*args, **kwargs):
            pass

        @classmethod
        def _teardown_class(cls):
            pass

    return MyTestCaseOk('test_method')


@nottest
def test_case_fail_on_test_method():
    class MyTestCaseFailsOnTestMethod(ContestoTestCase):
        driver = Mock()

        @classmethod
        def _setup_class(cls):
            pass

        def _setup_test(*args, **kwargs):
            pass

        def test_method(self):
            raise ValueError('123')

        def _teardown_test(*args, **kwargs):
            pass

        @classmethod
        def _teardown_class(cls):
            pass

    return MyTestCaseFailsOnTestMethod('test_method')


class TestOnTestErrorHandler(unittest.TestCase):
    def test_handler_should_not_be_called(self):
        broken_handler = Mock(side_effect=Exception())
        test_case = test_case_ok()
        test_case.add_handler('on_test_error', broken_handler)
        result = self.defaultTestResult()
        test_case.run(result)
        self.assertEqual(0, len(result.errors))
        self.assertEqual(broken_handler.call_count, 0)

    def test_ok_with_broken_handler(self):
        broken_handler = Mock(side_effect=Exception('Handler is broken'))
        test_case = test_case_fail_on_test_method()
        test_case.add_handler('on_test_error', broken_handler)
        result = self.defaultTestResult()
        test_case.run(result)
        self.assertEqual(1, len(result.errors))
        self.assertIn('ValueError(\'123\')', result.errors[0][1])
        self.assertNotIn('Handler is broken', result.errors[0][1])
        self.assertEqual(1, broken_handler.call_count)

    def test_few_handlers_call(self):
        handler_1 = Mock()
        handler_2 = Mock()
        test_case = test_case_fail_on_test_method()
        test_case.add_handler('on_test_error', handler_1)
        test_case.add_handler('on_test_error', handler_2)
        result = self.defaultTestResult()
        test_case.run(result)
        self.assertEqual(1, len(result.errors))
        self.assertIn('ValueError(\'123\')', result.errors[0][1])
        self.assertNotIn('Handler is broken', result.errors[0][1])
        self.assertEqual(handler_1.call_count, 1)
        self.assertEqual(handler_2.call_count, 1)
