def cached(function):
    cache = {}

    def wrapper(*args, **kwargs):
        key = str((args, sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        else:
            result = function(*args, **kwargs)
            cache[key] = result
            return result

    return wrapper


class cached_property(object):
    def __init__(self, method):
        self.method = method
        self.__name__ = method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.__name__, result)
        return result
