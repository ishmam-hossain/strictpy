import functools
from typing import Callable

from .helpers import (cross_check_types_of,
                      get_annotations_of,
                      ensure_type_hints_for,
                      ensure_keyword_only_arguments)


def strict(_wrapped_func=None, *,
           force_return_type_check: bool = True) -> Callable:
    def decorator_strict(decorated_func: Callable):
        ensure_type_hints_for(decorated_func)

        parameter_annotations: dict
        return_type_annotation: dict
        parameter_annotations, return_type_annotation = get_annotations_of(decorated_func)

        @functools.wraps(decorated_func)
        def wrapper_strict(*args, **kwargs):
            ensure_keyword_only_arguments(*args, **kwargs)
            cross_check_types_of(expected=parameter_annotations, received=kwargs)
            
            execution_result = decorated_func(*args, **kwargs)
            
            if force_return_type_check:
                cross_check_types_of(expected=return_type_annotation, received={'return': execution_result})
                
            return execution_result

        return wrapper_strict

    if _wrapped_func is None:
        return decorator_strict

    return decorator_strict(_wrapped_func)


