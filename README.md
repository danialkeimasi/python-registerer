# Fast Registry
A generic class that can be used to register classes or functions, with type hints support.

# Example
```py
from fast_registry import FastRegistry


class Animal:
    def talk(self):
        raise NotImplementedError


# create a registry that requires registered items to implement the Animal interface.
animal_registry = FastRegistry(Animal)

@animal_registry("dog")
class Dog:
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


# Installation

```bash
pip install fast-registry
```
