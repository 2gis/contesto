# coding: utf-8

import inspect
from functools import wraps

from contesto.globals import current_test
from contesto.utils import JSONSerializable


class Steps(list):
    def __init__(self):
        super(Steps, self).__init__()
        self.level = 0


class Step(JSONSerializable):
    def __init__(self, message):
        self.level = current_test._meta_info['steps'].level
        self.message = message
        current_test._meta_info['steps'].append(self)

    def __enter__(self):
        current_test._meta_info['steps'].level += 1
        print(str(self))

    def __exit__(self, exc_type, exc_val, exc_tb):
        current_test._meta_info['steps'].level -= 1

    def __repr__(self):
        return "<Step level=%s message=%s>" % (self.level, self.message)

    def __str__(self):
        indent = "    " * self.level
        return "%s%s" % (indent, self.message)


def step(message):
    def decorator(func):
        if is_step(func):
            return func

        setattr(func, "__step__", message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            arguments = dict(zip(inspect.signature(func).parameters.keys(), args))
            arguments.update(kwargs)
            with Step(message.format(**arguments)):
                return func(*args, **kwargs)
        return wrapper

    return decorator


def is_step(func):
    return hasattr(func, "__step__")
