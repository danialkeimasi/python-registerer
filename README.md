# Fast Registry
[![](https://img.shields.io/pypi/v/python-registerer.svg)](https://pypi.python.org/pypi/python-registerer/)
[![](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)

Everything you need to implement maintainable and easy to use registry patterns in your project.
# Installation

```sh
pip install fast-registry
```

# Register Classes
Register classes with the same interface, enforce the type check and enjoy the benefits of type hints:
```py
from registerer import Registerer


class Animal:
    def talk(self) -> None:
        raise NotImplementedError


# create a registry that requires registered items to implement the Animal interface:
animal_registry = Registerer(Animal)


@animal_registry.register("dog")
class Dog(Animal):
    def talk(self) -> None:
        return "woof"
```


# Register Functions
Register functions and benefit from the function annotations validator (optional):
```py
from registerer import Registerer, FunctionAnnotationValidator

database_registry = Registerer(
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
- [Class - Simple Type Checking](https://github.com/danialkeimasi/python-registerer/blob/main/examples/class.py)
- [Class - Custom Validator](https://github.com/danialkeimasi/python-registerer/blob/main/examples/class-with-custom-validator.py)
- [Function - Simple](https://github.com/danialkeimasi/python-registerer/blob/main/examples/function.py)
- [Function - With Type Annotation Validator](https://github.com/danialkeimasi/python-registerer/blob/main/examples/function-with-validator.py)
