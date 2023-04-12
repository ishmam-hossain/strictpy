import pytest

from src.strictpy.helpers import (check_type_hints,
                                  validate_arguments)
from src.strictpy.exceptions import (KeyWordsArgumentsOnlyException)


def test_check_type_hints_attribute_error():
    with pytest.raises(AttributeError):
        check_type_hints({'a': 'a', 'b': 'f'}, 1)
        check_type_hints(1, {'a': 'a', 'b': 'f'})


def test_validate_arguments_raise_keywords_only_exc():
    with pytest.raises(KeyWordsArgumentsOnlyException):
        validate_arguments(1, 2, 4)
        validate_arguments(4, '5', demo='value')
        validate_arguments('hello', demo='value')
