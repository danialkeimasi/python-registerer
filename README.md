# Fast Registry
[![](https://img.shields.io/pypi/v/fast-registry.svg)](https://pypi.python.org/pypi/fast-registry/)
[![](https://github.com/danialkeimasi/fast-registry/workflows/tests/badge.svg)](https://github.com/danialkeimasi/fast-registry/actions)
[![](https://img.shields.io/github/license/danialkeimasi/fast-registry.svg)](https://github.com/danialkeimasi/fast-registry/blob/master/LICENSE)

Everything you need to implement maintainable and easy to use registry patterns in your project.
# Installation

```sh
pip install fast-registry
```

# Register Classes
Register classes with the same interface, enforce the type check and enjoy the benefits of type hints:

![python fast-registry class example](https://raw.githubusercontent.com/danialkeimasi/python-fast-registry/main/images/class-registration-example.png)


# Register Functions
Register functions and benefit from the function annotations validator (optional):
```py
from fast_registry import FastRegistry, FunctionAnnotationValidator

database_registry = FastRegistry(
    validators=[
        FunctionAnnotationValidator(annotations=[("name", str)]),
    ]
)

@database_registry.register("sqlite")
def sqlite_database_connection(name: str):
    return f"sqlite connection {name}"
```

# Create Custom Validators
By Creating a subclass of `RegistryValidator`, you can create your own validators to check registered classes/functions if you need to.

# Examples
- [Class - Simple Type Checking](https://github.com/danialkeimasi/python-fast-registry/blob/main/examples/class.py)
- [Class - Custom Registration](https://github.com/danialkeimasi/python-fast-registry/blob/main/examples/class-with-custom-validator.py)
- [Function - Simple](https://github.com/danialkeimasi/python-fast-registry/blob/main/examples/function.py)
- [Function - With Type Annotation Validation](https://github.com/danialkeimasi/python-fast-registry/blob/main/examples/function-with-validator.py)
