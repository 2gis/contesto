from mock import Mock
from contesto.basis.test_case import UnittestContestoTestCase
from contesto import config
import os

config.add_config_file(os.path.abspath(os.path.dirname(__file__)) + "/data/config/session.ini")


class SessionTestCase(UnittestContestoTestCase):
    def setUp(self):
        self.driver = Mock()

    def test_true_shared_session(self):
        self.assertEqual(config.session["shared"], True)