<div align="center">
    <p >
      <img src="assets/strictpy_logo.png" />
    </p>
    <h1>Strictpy</h1>
    
</div>

[![Publish to PyPi](https://github.com/ishmam-hossain/strictpy/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/ishmam-hossain/strictpy/actions/workflows/pypi-publish.yml)
[![Publish to Test PyPi](https://github.com/ishmam-hossain/strictpy/actions/workflows/test-pypi-publish.yml/badge.svg)](https://github.com/ishmam-hossain/strictpy/actions/workflows/test-pypi-publish.yml)

This library provides a simple decorator that allows you to enforce strict type 
checking in you everyday cPython functions based on the type hint of the function parameters.


### What to expect from this decorator?

When you use this decorator in your function, you have to keep in mind a couple of things-
1. This strictly requires type hinting your function parameters & return value
2. If you don't provide type hinting, you'll see some custom exceptions being raised named `TypeHintMissingError`
3. You can skip the return value strict check, if you want. But function parameters are always type checked
4. If you pass type hinting but the hint don't match with the value type, you'll get a `TypeMismatchError` 
5. You must call your function with Keyword arguments, otherwise you'll get a `PositionalArgumentsNotAllowedException` 

Each error/exception will have helpful message to help you identify what you need to do.


### Installation
You can simply install the latest version with this command: 
```python
pip install strictpy
```
If you want any specific older version:
```python
pip install strictpy==1.0.0
```

### Usage
The usage is pretty simple and intuitive. We just need to have our functions
decorated with `@strict`.

Let's start with simple example:

```python
from strictpy import strict

@strict
def some_function(x: int, y: int) -> int:
    return x * y

some_function(x=5, y=6)
```
This will lead to execution of the function with no visible difference as all the arguments and the return value is
type hinted.
Also, the function is called with Keyword arguments, which is a must if you use `@strict` decorator.


Now, let's see an example what happens if type hints are missing:
```python
from strictpy import strict

@strict
def some_function(x: int, y: int):
    return x * y

some_function(x=5, y=6)
```

If you run this code, you'll get the following exception because the return type hint is missing:

```python
...
File "/Users/ishmam/PycharmProjects/strict-py/src/strictpy/helpers.py", line 14, in ensure_return_type_hint
    raise TypeHintMissingError("return type hint cannot be empty.")
strictpy.exceptions.TypeHintMissingError: return type hint cannot be empty.
```

Although, you can skip check for return type check like this:
```python
from strictpy import strict

@strict(force_return_type_check=False)
def some_function(x: int, y: int):
    return x * y

some_function(x=5, y=6)
```

This will ignore the return value missing type hint.

In this last example you'll see the exception that is raised when the function
is called with Positional arguments:

```python
from strictpy import strict

@strict(force_return_type_check=False)
def some_function(x: int, y: int):
    return x * y

some_function(5, y=6) # x is positional
```

Raised exception:
```python
File "/Users/ishmam/PycharmProjects/strict-py/src/strictpy/helpers.py", line 33, in ensure_keyword_only_arguments
    raise PositionalArgumentsNotAllowedException(
strictpy.exceptions.PositionalArgumentsNotAllowedException: Only keyword arguments are expected, 1 were passed as positional arguments.

```