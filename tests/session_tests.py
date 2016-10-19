import unittest
try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock
from contesto import ContestoTestCase
from contesto import config
import os


def mktest():
    class TestCase(ContestoTestCase):
        _start_driver = Mock(
            side_effect=[
                Mock(capabilities={}),
                Mock(capabilities={})
            ])

        def runTest(self):
            pass
    test = TestCase()
    return test


class NoMixinSessionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._default_config = config
        config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/session.ini")

    @classmethod
    def tearDownClass(cls):
        global config
        config = cls._default_config

    def test_true_shared_session(self):
        testcase = mktest()
        testcase.setUpClass()
        testcase._init_context()
        testcase.setUp()
        driver1 = testcase.driver
        testcase.setUp()
        testcase._init_context()
        driver2 = testcase.driver
        self.assertEqual(driver1, driver2)
        self.assertTrue(config.session["shared"])


class NoMixinNoSharedSessionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._default_shared_session_value = config.session["shared"]
        config.session["shared"] = False

    @classmethod
    def tearDownClass(cls):
        config.session["shared"] = cls._default_shared_session_value

    def test_false_shared_session(self):
        testcase = mktest()
        testcase.setUpClass()
        testcase._init_context()
        testcase.setUp()
        driver1 = testcase.driver
        testcase._init_context()
        testcase.setUp()
        driver2 = testcase.driver
        self.assertNotEqual(driver1, driver2)
        self.assertFalse(config.session["shared"])
