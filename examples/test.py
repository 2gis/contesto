# coding: utf-8

import os

from contesto import ContestoTestCase, config
config.add_config_file(os.path.join(os.path.dirname(__file__), "config.ini"))

from examples.page import CityPage


class TestExample(ContestoTestCase):
    def setUp(self):
        super(TestExample, self).setUp()
        self.driver.get("http://2gis.ru")
        self.page = CityPage(self.driver)

    def test_example(self):
        self.page.search_bar().search("1")
        results_count = self.page.search_results().results_count()
        self.assertGreater(results_count, 0)
