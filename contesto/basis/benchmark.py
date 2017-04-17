# -*- coding: utf-8 -*-
from contesto import ContestoTestCase, config
from contesto.utils.log import log


class BenchmarkBaseCase(ContestoTestCase):
    metrics = {}

    def __init__(self, test_name='runTest'):
        super(BenchmarkBaseCase, self).__init__(test_name)
        self.run_count = config.benchmark.get('run_count', 1)

        self._set_up_iter = self.setUp
        self._tear_down_iter = self.tearDown

        self.setUp = self._do_nothing
        self.tearDown = self._do_nothing

        self._single_method = getattr(self, self._testMethodName)
        setattr(self, self._testMethodName, self.run_multiple_times)

        self.metrics[self._testMethodName] = {}

    def _do_nothing(self):
        log.debug('Skip setUp / tearDown for \'{}\' '
                  '(Will be started for each benchmark iteration)'.format(self._testMethodName))

    def run_multiple_times(self):
        for i in range(1, self.run_count + 1):
            log.info('Benchmark \'{}\' iter {}'.format(self._testMethodName, i))
            try:
                self._set_up_iter()
                res = self._single_method()
                self._tear_down_iter()
            except:
                log.exception('Benchmark \'{}\' iter {} exception:'.format(self._testMethodName, i))
                raise
        return res
