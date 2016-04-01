# coding: utf-8
import unittest

try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock

from multiprocessing import Queue as MultiprocessQueue, Process
from threading import Thread

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


from contesto import ContestoTestCase, config
from contesto.globals import current_test


def mktest():
    class TestCase(ContestoTestCase):
        @staticmethod
        def _create_session(cls):
            return Mock()

        def test_1(self):
            self.assertEqual(self, current_test)

        def test_2(self):
            self.assertEqual(self, current_test)

    return TestCase


def init_context(q, test):
    test._init_context()
    q.put("Done")


class TestCurrentTest(unittest.TestCase):
    def setUp(self):
        self._config_session_shared = config.session["shared"]
        config.session["shared"] = False

    def tearDown(self):
        config.session["shared"] = self._config_session_shared

    def test_current_test_set(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        self.assertRaises(RuntimeError, current_test)
        test_1.run()
        self.assertRaises(RuntimeError, current_test)

    def test_current_test_changes(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        test_2 = testcase('test_2')
        result = unittest.TestResult()
        test_1.run(result)
        test_2.run(result)
        self.assertEqual(2, result.testsRun)
        self.assertEqual([], result.errors)

    def test_processes_dont_share_current_test(self):
        testcase = mktest()
        test = testcase("test_1")
        q = MultiprocessQueue()
        self.assertRaises(RuntimeError, current_test)
        Process(target=init_context, args=(q, test)).start()
        self.assertEqual("Done", q.get())
        self.assertRaises(RuntimeError, current_test)

    def test_threads_share_current_test(self):
        testcase = mktest()
        test = testcase("test_1")
        q = Queue()
        Thread(target=init_context, args=(q, test)).start()
        self.assertEqual("Done", q.get())
        self.assertEqual(test, current_test)
        test._free_context()
        self.assertRaises(RuntimeError, current_test)

    def test_current_test_class(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        test_1._init_context()
        self.assertIsInstance(current_test, testcase)
        test_1._free_context()
