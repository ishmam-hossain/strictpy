class TypeMismatchError(Exception):
    """Raise when the function signature type hint and the received type does not match"""


class TypeHintMissingError(Exception):
    """Raise when type hint is not explicitly given"""


class PositionalArgumentsNotAllowedException(Exception):
    """Raise when positional arguments are sent to the strict decorated function"""
