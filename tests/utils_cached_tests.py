from utils.cached import cached, cached_property

call_counter = 0


@cached
def some_global_func(foo, bar):
    global call_counter
    call_counter += 1
    return foo + bar


class Foo(object):
    def __init__(self):
        self.call_counter = 0

    @cached
    def some_function_without_params_that_returns_three(self):
        self.call_counter += 1
        return 1 + 2

    @cached
    def some_function_with_one_param_that_returns_it_squared(self, bar):
        self.call_counter += 1
        return bar ** 2

    @cached
    def some_function_with_several_params_that_returns_them_sum(self, *args):
        self.call_counter += 1
        result = 0
        for param in args:
            result += param
        return result

    @cached
    def some_function_with_two_params_that_returns_them_string_representation(self, bar, baz):
        self.call_counter += 1
        return "bar=%s,baz=%s" % (bar, baz)

    @cached_property
    def some_property_that_equals_31(self):
        self.call_counter += 1
        return 31


def test_cached_global_func():
    global call_counter
    assert call_counter == 0
    assert some_global_func(1, 8) == 9
    assert call_counter == 1
    assert some_global_func(1, 8) == 9
    assert call_counter == 1


def test_cached_function_without_parameters():
    foo = Foo()
    assert foo.call_counter == 0
    assert foo.some_function_without_params_that_returns_three() == 3
    assert foo.call_counter == 1
    assert foo.some_function_without_params_that_returns_three() == 3
    assert foo.call_counter == 1


def test_cached_function_with_one_parameter():
    foo = Foo()
    assert foo.call_counter == 0
    assert foo.some_function_with_one_param_that_returns_it_squared(2) == 4
    assert foo.call_counter == 1
    assert foo.some_function_with_one_param_that_returns_it_squared(2) == 4
    assert foo.call_counter == 1
    assert foo.some_function_with_one_param_that_returns_it_squared(5) == 25
    assert foo.call_counter == 2
    assert foo.some_function_with_one_param_that_returns_it_squared(5) == 25
    assert foo.call_counter == 2


def test_cached_function_with_several_parameters():
    foo = Foo()
    assert foo.call_counter == 0
    assert foo.some_function_with_several_params_that_returns_them_sum() == 0
    assert foo.call_counter == 1
    assert foo.some_function_with_several_params_that_returns_them_sum() == 0
    assert foo.call_counter == 1
    assert foo.some_function_with_several_params_that_returns_them_sum(2) == 2
    assert foo.call_counter == 2
    assert foo.some_function_with_several_params_that_returns_them_sum(2) == 2
    assert foo.call_counter == 2
    assert foo.some_function_with_several_params_that_returns_them_sum(2, 3, 5, 7, 11, 13, 17, 19) == 77
    assert foo.call_counter == 3
    assert foo.some_function_with_several_params_that_returns_them_sum(2, 3, 5, 7, 11, 13, 17, 19) == 77
    assert foo.call_counter == 3


def test_cached_property():
    foo = Foo()
    assert foo.call_counter == 0
    assert foo.some_property_that_equals_31 == 31
    assert foo.call_counter == 1
    assert foo.some_property_that_equals_31 == 31
    assert foo.call_counter == 1


def test_cached_function_with_named_parameters():
    foo = Foo()
    assert foo.call_counter == 0
    assert foo.some_function_with_two_params_that_returns_them_string_representation(bar=1, baz=2) == "bar=1,baz=2"
    assert foo.call_counter == 1
    assert foo.some_function_with_two_params_that_returns_them_string_representation(bar=1, baz=2) == "bar=1,baz=2"
    assert foo.call_counter == 1
    assert foo.some_function_with_two_params_that_returns_them_string_representation(baz=2, bar=1) == "bar=1,baz=2"
    assert foo.call_counter == 1
    assert foo.some_function_with_two_params_that_returns_them_string_representation(bar=3, baz=4) == "bar=3,baz=4"
    assert foo.call_counter == 2
    assert foo.some_function_with_two_params_that_returns_them_string_representation(bar=3, baz=4) == "bar=3,baz=4"
    assert foo.call_counter == 2
