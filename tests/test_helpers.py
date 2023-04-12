import pytest
from typing import List

from src.strictpy import helpers
from src.strictpy import exceptions

import inspect


def test_ensure_return_type_hint_with_return_hint():
    def some_function() -> int:
        return 5

    sig = inspect.signature(some_function)
    assert helpers.ensure_return_type_hint(sig) is None


def test_ensure_return_type_hint_without_return_hint():
    def some_function():
        return "Hello World"

    sig = inspect.signature(some_function)
    with pytest.raises(exceptions.TypeHintMissingError):
        helpers.ensure_return_type_hint(sig)


def test_ensure_return_type_hint_with_None_as_return_hint():
    def some_function() -> None:
        return

    sig = inspect.signature(some_function)
    assert helpers.ensure_return_type_hint(sig) is None


def test_ensure_return_type_hint_with_non_empty_return_hint():
    def some_function() -> str:
        return "Hello World"

    sig = inspect.signature(some_function)
    assert helpers.ensure_return_type_hint(sig) is None


def test_ensure_param_type_hints_all_hints_specified():
    def some_function(x: int, y: str) -> None:
        pass

    sig = inspect.signature(some_function)
    assert helpers.ensure_param_type_hints(sig) is None


def test_ensure_param_type_hints_some_hints_specified():
    def some_function(x: int, y, z: float) -> None:
        pass

    sig = inspect.signature(some_function)
    with pytest.raises(exceptions.TypeHintMissingError):
        helpers.ensure_param_type_hints(sig)


def test_ensure_param_type_hints_no_hints_specified():
    def some_function(x, y, z) -> None:
        pass

    sig = inspect.signature(some_function)
    with pytest.raises(exceptions.TypeHintMissingError):
        helpers.ensure_param_type_hints(sig)


def test_ensure_param_type_hints_empty_hint_specified():
    def some_function(x: int, y: str, z) -> None:
        pass

    sig = inspect.signature(some_function)
    with pytest.raises(exceptions.TypeHintMissingError):
        helpers.ensure_param_type_hints(sig)


def test_ensure_keyword_only_arguments_no_args():
    assert helpers.ensure_keyword_only_arguments() is None


def test_ensure_keyword_only_arguments_only_keyword_args():
    assert helpers.ensure_keyword_only_arguments(x=1, y=2) is None


def test_ensure_keyword_only_arguments_mixture_of_args():
    with pytest.raises(exceptions.PositionalArgumentsNotAllowedException):
        helpers.ensure_keyword_only_arguments(1, y=2)


def test_ensure_keyword_only_arguments_only_positional_args():
    with pytest.raises(exceptions.PositionalArgumentsNotAllowedException):
        helpers.ensure_keyword_only_arguments(1, 2, 3)


def test_ensure_keyword_only_arguments_single_positional_arg():
    with pytest.raises(exceptions.PositionalArgumentsNotAllowedException):
        helpers.ensure_keyword_only_arguments(1)


def test_cross_check_types_of():
    # Test with matching types
    expected = {'a': int, 'b': str}
    received = {'a': 1, 'b': 'hello'}
    helpers.cross_check_types_of(expected, received)  # Should not raise any exception

    # Test with mismatched type
    expected = {'a': int, 'b': str}
    received = {'a': 'hello', 'b': 'world'}
    with pytest.raises(exceptions.TypeMismatchError):
        helpers.cross_check_types_of(expected, received)

    # Test with missing parameter in received
    expected = {'a': int, 'b': str}
    received = {'a': 1}
    with pytest.raises(exceptions.TypeMismatchError):
        helpers.cross_check_types_of(expected, received)

    # Test with extra parameter in received
    expected = {'a': int, 'b': str}
    received = {'a': 1, 'b': 'hello', 'c': True}
    helpers.cross_check_types_of(expected, received)  # Should not raise any exception


def test_get_annotations_of():

    def add_numbers(a: int, b: int) -> int:
        return a + b

    def get_list() -> List[str]:
        return ['foo', 'bar']

    def function_with_no_annotations():
        pass

    # Test with a function that has annotations for parameters and return type
    parameter_annotations, return_type_annotation = helpers.get_annotations_of(add_numbers)
    assert parameter_annotations == {'a': int, 'b': int}
    assert return_type_annotation == {'return': int}

    # Test with a function that has an annotation for return type but no annotations for parameters
    parameter_annotations, return_type_annotation = helpers.get_annotations_of(get_list)
    assert parameter_annotations == {}
    assert return_type_annotation == {'return': List[str]}

    # raises KeyError
    # to reach to this stage, the decorated function must pass ensure_type_hints_for
    with pytest.raises(KeyError):
        _, _ = helpers.get_annotations_of(function_with_no_annotations)

