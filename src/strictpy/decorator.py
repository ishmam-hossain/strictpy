import functools
from typing import Callable

from .helpers import (check_type_hints,
                      get_annotations_of,
                      validate_func_signature,
                      validate_func_arguments)


def strict(_wrapped_func=None,
           *,
           force_return_type_check: bool = True) -> Callable:
    def decorator_strict(func: Callable):
        parameter_annotations: dict
        return_type_annotation: dict

        validate_func_signature(func=func)
        parameter_annotations, return_type_annotation = get_annotations_of(func)

        @functools.wraps(func)
        def wrapper_strict(*args, **kwargs):
            validate_func_arguments(*args, **kwargs)
            check_type_hints(expected=parameter_annotations, received=kwargs)
            value_returned = func(*args, **kwargs)
            if force_return_type_check:
                check_type_hints(expected=return_type_annotation, received={'return': value_returned})
            return value_returned

        return wrapper_strict

    if _wrapped_func is None:
        return decorator_strict

    return decorator_strict(_wrapped_func)


