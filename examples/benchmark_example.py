# -*- coding: utf-8 -*-

from contesto import BenchmarkBaseCase


class TestBenchmarkExamples(BenchmarkBaseCase):
    @classmethod
    def setUpClass(cls):
        print('\nmake setupclass')

    @classmethod
    def tearDownClass(cls):
        print('make teardownclass')

    def setUp(self):
        print('\tmake setup')

    def tearDown(self):
        print('\tmake teardown')

    def test_benchmark_app_start(self):
        """
        AppStart scenario example ("do nothing")
        """
        print('\t\tHey! I\'m app-start scenario!')

    def test_benchmark_search(self):
        """
        Search scenario example
        """
        print('\t\tHey! I\'m search scenario!')
        print('\t\tSearching \'beer\'')
