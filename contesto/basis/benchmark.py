# -*- coding: utf-8 -*-

from contesto import ContestoTestCase, config
from contesto.utils.log import log


class BenchmarkBaseCase(ContestoTestCase):
    def __init__(self, test_name='runTest'):
        super(BenchmarkBaseCase, self).__init__(test_name)
        self.run_count = config.benchmark.get('run_count', 1)
        self._single_method = getattr(self, self._testMethodName)
        setattr(self, self._testMethodName, self.run_multiple_times)

    def run_multiple_times(self):
        for i in range(1, self.run_count + 1):
            log.debug('Benchmark iter {}'.format(i))
            try:
                res = self._single_method()
            except:
                log.exception('Benchmark iter {} exception:'.format(i))
                raise
        return res
