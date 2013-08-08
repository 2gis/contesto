from contesto.utils.extending import AutoExtendingSelectors


class Foo(object):
    __metaclass__ = AutoExtendingSelectors
    selectors = {
        'a': 1,
    }


class Bar(Foo):
    selectors = {
        'b': 2,
    }


class Baz(Bar):
    selectors = {
        'a': 3,
        'c': 4,
    }


class Qux(Baz):
    selectors = {}


def dict_equals(dict1, dict2):
    if len(dict1) != len(dict2):
        return False
    else:
        for key in dict1:
            if key not in dict2 or dict1[key] != dict2[key]:
                return False
        return True


def test_autoextending_selectors():
    foo = Foo()
    bar = Bar()
    baz = Baz()
    qux = Qux()
    assert dict_equals(foo.selectors, {'a': 1})
    assert dict_equals(bar.selectors, {'a': 1, 'b': 2})
    assert dict_equals(baz.selectors, {'a': 3, 'b': 2, 'c': 4})
    assert dict_equals(qux.selectors, {'a': 3, 'b': 2, 'c': 4})
