try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock
from contesto.basis.page import WebPage, Page, BasePage
import unittest


class PageTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = Mock()
        self.driver.page_source = "source"
        self.driver.current_url = "http://current_url/"

    def test_page(self):
        page = Page(self.driver)
        self.assertEqual(page.get_source(), "source")

    def test_web_page(self):
        page = WebPage(self.driver)
        self.assertEqual(page.url, "http://current_url/")

    def test_backward_compatibility_base_page(self):
        page = BasePage(self.driver)
        self.assertEqual(page.url, "http://current_url/")
