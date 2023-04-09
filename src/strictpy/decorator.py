import functools
from typing import Callable

from src.strictpy.helpers import (validate_arguments,
                                  check_type_hints)


def strict(_wrapped_func=None,
           *,
           force_return_type_check: bool = True) -> Callable:
    def decorator_strict(func):
        func_annotations: dict = func.__annotations__
        return_type_annotation: dict = {'return': func_annotations.pop('return')}
        parameter_annotations: dict = func_annotations

        @functools.wraps(func)
        def wrapper_strict(*args, **kwargs):
            validate_arguments(*args, **kwargs)
            check_type_hints(expected=parameter_annotations, received=kwargs)
            value_returned = func(*args, **kwargs)
            if force_return_type_check:
                check_type_hints(expected=return_type_annotation, received={'return': value_returned})
            return value_returned

        return wrapper_strict

    if _wrapped_func is None:
        return decorator_strict

    return decorator_strict(_wrapped_func)


