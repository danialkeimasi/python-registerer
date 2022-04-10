# Fast Registry
[![](https://img.shields.io/pypi/v/fast-registry.svg)](https://pypi.python.org/pypi/fast-registry/)
[![](https://github.com/danialkeimasi/fast-registry/workflows/tests/badge.svg)](https://github.com/danialkeimasi/fast-registry/actions)
[![](https://img.shields.io/github/license/danialkeimasi/fast-registry.svg)](https://github.com/danialkeimasi/fast-registry/blob/master/LICENSE)

A generic class that can be used to register classes or functions, with type hints support.
# Installation

```bash
pip install fast-registry
```

# Register Classes
You can enforce types on your concrete classes, and also use type hints on your text editors:

```py
from fast_registry import FastRegistry


class Animal:
    def talk(self):
        raise NotImplementedError


# create a registry that requires registered items to implement the Animal interface:
animal_registry = FastRegistry(Animal)

@animal_registry("dog")
class Dog(Animal):
    def talk(self):
        return "woof"
```

```sh
>> animal_registry["dog"]
<class '__main__.Dog'>

>> animal_registry["dog"]()
<__main__.Dog object at 0x7fda96d3b310>

>> animal_registry["dog"]().talk()
'woof'
```

# Register Functions

You can also use this tool to register functions:
```py
from fast_registry import FastRegistry


registry = FastRegistry()


@registry("foo")
def foo():
    return "bar"
```

```sh
>>> registry["foo"]
<function foo at 0x7f803c989fc0>

>>> registry["foo"]()
'bar'
```
