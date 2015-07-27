import unittest

from contesto.utils.extending import AutoExtendingSelectors

"""
Trick to create class with metaclass
for both python 2 and 3. It's like

2:
class Foo(object):
    __metaclass__=AutoExtendingSelectors
    selectors: {
        'a': 1
    }

3:
class Foo(metaclass=AutoExtendingSelectors):
    selectors: {
        'a': 1
    }
"""
Foo = AutoExtendingSelectors("Foo", (), {
    'selectors': {
        'a': 1
    }
})


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


class AutoextendingSelectorsTest(unittest.TestCase):
    def test_autoextending_selectors(self):
        foo = Foo()
        bar = Bar()
        baz = Baz()
        qux = Qux()
        self.assertEqual({'a': 1}, foo.selectors)
        self.assertEqual({'a': 1, 'b': 2}, bar.selectors)
        self.assertEqual({'a': 3, 'b': 2, 'c': 4}, baz.selectors)
        self.assertEqual({'a': 3, 'b': 2, 'c': 4}, qux.selectors)
