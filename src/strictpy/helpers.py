from .exceptions import (KeyWordsArgumentsOnlyException,
                         TypeMismatchException)


def validate_arguments(*args: tuple, **_: dict) -> None:
    if (positional_args_len := len(args)) > 0:
        raise KeyWordsArgumentsOnlyException(
            f"Only keyword arguments are expected, {positional_args_len} were passed as positional arguments."
        )


def check_type_hints(expected: dict, received: dict) -> None:
    for param, expected_type in expected.items():
        if not isinstance(received.get(param), expected_type):
            raise TypeMismatchException(
                f"Expected type of '{param}' is {expected_type}, "
                f"got {type(received.get(param))} instead."
            )

