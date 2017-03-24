# coding: utf-8

try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock

import unittest

from contesto import BenchmarkBaseCase, config


def make():
    class TestFakeBenchmark(BenchmarkBaseCase):
        mock_method = Mock()
        mock_setup = Mock()
        mock_teardown = Mock()

        @classmethod
        def _create_session(cls, *args, **kwargs):
            return Mock()

        def test_method(self):
            self.mock_method()

        def setUp(self):
            self.mock_setup()

        def tearDown(self):
            self.mock_teardown()

    return TestFakeBenchmark('test_method')


class TestBenchmarkBaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._config_benchmark_run_count = config.benchmark["run_count"]
        config.benchmark["run_count"] = 5

    @classmethod
    def tearDownClass(cls):
        config.benchmark["run_count"] = cls._config_benchmark_run_count

    def test_multiple_run(self):
        benchmark = make()
        benchmark.run()
        self.assertEqual(benchmark.mock_method.call_count, 5)
        self.assertEqual(benchmark.mock_setup.call_count, 5)
        self.assertEqual(benchmark.mock_teardown.call_count, 5)
