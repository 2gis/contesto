def before(*args):
    class Before(object):
        def __init__(self, function, *args):
            self.function = function
            self.__name__ = function.__name__
            self.__doc__ = function.__doc__
            self.before = [func for func in list(args) if callable(func)]

        def __call__(self, *args):
            for func in self.before:
                func()
            return self.function(*args)

    def decorator(function):
        return Before(function, *args)

    return decorator


def after(*args):
    class After(object):
        def __init__(self, function, *args):
            self.function = function
            self.__name__ = function.__name__
            self.__doc__ = function.__doc__
            self.after = [func for func in list(args) if callable(func)]

        def __call__(self, *args):
            result = self.function(*args)
            for func in self.after:
                func()
            return result

    def decorator(function):
        return After(function, *args)

    return decorator
