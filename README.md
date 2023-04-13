<div align="center">
    <p >
      <img src="assets/strictpy_logo.png" />
    </p>
    <h1>Strictpy</h1>
    
    [![Publish to PyPi](https://github.com/ishmam-hossain/strictpy/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/ishmam-hossain/strictpy/actions/workflows/pypi-publish.yml)
</div>

This library provides a simple decorator that allows you to enforce strict type 
checking in you everyday cPython functions based on the type hint of the function parameters.

The usage is pretty simple and intuitive. We just need to have our functions
decorated with `@strict`.

Let's start with simple example where the function does not have any type hints:

```python
from strictpy import strict

@strict
def some_function(x, y):
    return x * y
```

This will raise an error called `TypeHintMissingError` with detailed message of what is expected.

If we now rewrite the function this way, it will run as usual:

```python
from strictpy import strict

@strict
def some_function(x: int, y: int) -> int:
    return x * y
```
