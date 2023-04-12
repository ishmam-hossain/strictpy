import inspect
from typing import Callable, get_type_hints

from .exceptions import (TypeMismatchError,
                         TypeHintMissingError,
                         PositionalArgumentsNotAllowedException)

_EMPTY = inspect._empty


def ensure_return_type_hint(func_signature: inspect.Signature) -> None:
    if func_signature.return_annotation is not _EMPTY:
        return
    raise TypeHintMissingError("return type hint cannot be empty.")


def ensure_param_type_hints(func_signature: inspect.Signature) -> None:
    for name in func_signature.parameters:
        if func_signature.parameters[name].annotation is not _EMPTY:
            continue
        raise TypeHintMissingError(f"parameter type hint cannot be empty for '{name}'")


def ensure_type_hints_for(decorated_func: Callable) -> None:
    func_signature = inspect.signature(decorated_func)
    ensure_param_type_hints(func_signature)
    ensure_return_type_hint(func_signature)


def ensure_keyword_only_arguments(*args: tuple, **_: dict) -> None:
    if (positional_args_len := len(args)) > 0:
        raise PositionalArgumentsNotAllowedException(
            f"Only keyword arguments are expected, "
            f"{positional_args_len} were passed as positional arguments."
        )


def cross_check_types_of(expected: dict, received: dict) -> None:
    for param, expected_type in expected.items():
        if not isinstance(received.get(param), expected_type):
            raise TypeMismatchError(
                f"Expected type of '{param}' is {expected_type}, "
                f"got {type(received.get(param))} instead."
            )


def get_annotations_of(func: Callable) -> tuple[dict, dict]:
    func_annotations: dict = get_type_hints(func)
    return_type_annotation: dict = {'return': func_annotations.pop('return')}
    parameter_annotations: dict = func_annotations
    return parameter_annotations, return_type_annotation
