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
from contesto.globals import current_test, _context


def mktest():
    class TestCase(ContestoTestCase):
        @staticmethod
        def _create_session(cls):
            return Mock()

        def test_1(self):
            pass

        def test_2(self):
            pass

    return TestCase


def helper(q, test):
    test.setUp()
    q.put("Done")


class TestCurrentTest(unittest.TestCase):
    def setUp(self):
        self._config_session_shared = config.session["shared"]
        config.session["shared"] = False

    def tearDown(self):
        config.session["shared"] = self._config_session_shared

    def test_current_test_setup_and_teardown(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        self.assertRaises(RuntimeError, current_test)
        test_1.setUp()
        self.assertEqual(test_1, current_test)
        test_1.tearDown()
        self.assertRaises(RuntimeError, current_test)

    def test_current_test_changes(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        test_2 = testcase('test_2')
        test_1.setUp()
        self.assertEqual(test_1, current_test)
        test_1.tearDown()
        test_2.setUp()
        self.assertEqual(test_2, current_test)
        test_2.tearDown()

    def test_processes_dont_share_current_test(self):
        testcase = mktest()
        test = testcase("test_1")
        q = MultiprocessQueue()
        Process(target=helper, args=(q, test)).start()
        self.assertEqual("Done", q.get())
        self.assertRaises(RuntimeError, current_test)

    def test_threads_share_current_test(self):
        testcase = mktest()
        test = testcase("test_1")
        q = Queue()
        Thread(target=helper, args=(q, test)).start()
        self.assertEqual("Done", q.get())
        test.tearDown()
        self.assertRaises(RuntimeError, current_test)

    def test_current_test_class(self):
        testcase = mktest()
        test_1 = testcase('test_1')
        test_1.setUp()
        self.assertIsInstance(current_test, testcase)
        test_1.tearDown()
