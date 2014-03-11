from mock import Mock
from contesto.basis.test_case import UnittestContestoTestCase
from contesto import config
import os

config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/session.ini")


class NoMixinSessionTest(UnittestContestoTestCase):
    @classmethod
    def setUpClass(cls):
        cls._start_driver = Mock()
        super(NoMixinSessionTest, cls).setUpClass()

    def test_true_shared_session(self):
        driver1 = self.driver
        self._start_driver = Mock()
        self.setUp()
        driver2 = self.driver
        self.assertEqual(driver1, driver2)
        self.assertTrue(config.session["shared"])


class NoMixinNoSharedSessionTest(UnittestContestoTestCase):
    @classmethod
    def setUpClass(cls):
        config.session["shared"] = False
        cls._start_driver = Mock()
        super(NoMixinNoSharedSessionTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        config.session["shared"] = True

    def test_false_shared_session(self):
        driver1 = self.driver
        self._start_driver = Mock()
        self.setUp()
        driver2 = self.driver
        self.assertNotEqual(driver1, driver2)
        self.assertFalse(config.session["shared"])