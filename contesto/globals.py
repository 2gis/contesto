# coding: utf-8

from contesto.utils import LocalProxy

_test_ctx_err_msg = '''\
Working outside of test context.

This typically means that you attempted to use functionality that needed
an active test.\
'''


class Context(object):
    test = None

_context = Context()


def _find_current_test():
    if _context.test is None:
        raise RuntimeError(_test_ctx_err_msg)
    return _context.test


current_test = LocalProxy(lambda: _find_current_test())
