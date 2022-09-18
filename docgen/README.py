"""# Registerer
[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![ci](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![codecov](https://codecov.io/gh/danialkeimasi/python-registerer/branch/main/graph/badge.svg?token=Q5MG14RKJL)](https://codecov.io/gh/danialkeimasi/python-registerer)
[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)


Implement maintainable and easy to use registry patterns in your project.

TLDR; Write this:
"""
import registerer

command_handler_registry = registerer.Registerer()


@command_handler_registry.register
def hello(args):
    return "hello to you too"


@command_handler_registry.register
def info(args):
    return "how can i help you?"


@command_handler_registry.register
def play(args):
    return "let me play a song for you"


command = "info"
args = {}
assert command_handler_registry[command](args) == "how can i help you?"
"""
Instead of this, which violates the Open-Closed Principle (OCP):
"""


def hello(args):
    return "hello to you too"


def info(args):
    return "how can i help you?"


def play(args):
    return "let me play a song for you"


def command_handler(command, args):
    if command == "hello":
        return hello(args)
    if command == "info":
        return info(args)
    if command == "play":
        return play(args)


command = "info"
args = {}
assert command_handler(command, args) == "how can i help you?"
"""
## Installation

```sh
pip install registerer
```

## Usage

In order to use registerer, you need to instantiate from the `registerer.Registerer`.

There is several optional arguments you can pass to the `Registerer` constructor
to manage how registry object should behave (Read more in reference section).

let's create a registry:
"""

import abc


class Animal(abc.ABC):
    is_wild: bool = None

    @abc.abstractmethod
    def walk(self):
        pass


# Animal class registry
animal_registry = registerer.Registerer(
    parent_class=Animal,
    max_size=5,  # only 5 items can register
    validators=[
        registerer.RegistryValidator(
            lambda item: item.is_wild is False,  # check passed if returns True
            error="can't register wild animal.",
        ),
    ],
)


"""
Now with `animal_registry` you can register your classes:
"""


# use the name of class as unique identifier:
@animal_registry.register
class Sheep(Animal):
    is_wild = False

    def walk(self):
        return "sheep walks"


# use your custom slug as unique identifier:
@animal_registry.register("kitty")
class Cat(Animal):
    is_wild = False

    def walk(self):
        return "cat walks"


assert animal_registry["Sheep"] == Sheep
assert animal_registry["kitty"] == Cat

assert animal_registry.items == [Sheep, Cat]
assert animal_registry._registry_dict == {"Sheep": Sheep, "kitty": Cat}

assert animal_registry["Sheep"]().walk() == "sheep walks"
assert animal_registry["kitty"]().walk() == "cat walks"
"""
The `register` method will also set an attribute on the registered item as `registry_slug`.  
So, in last example we have:

"""
assert Cat.registry_slug == "kitty"
assert animal_registry["kitty"].registry_slug == "kitty"

"""
if you need to add attributes on the registered item on registration (it's optional), you can pass kwargs to the `register` method.  
This is useful when registering functions. for example:
"""

# function registry
test_database_registry = registerer.Registerer(
    validators=[
        registerer.RegistryValidator(
            lambda item: item.db_type == "test",
        ),
    ]
)

# use the name of function as unique identifier:
@test_database_registry.register(db_type="test")
def sqlite(name: str):
    return f"sqlite connection {name}"


# use your custom slug as unique identifier:
@test_database_registry.register("postgresql", db_type="test")
def postgresql_test(name: str):
    return f"postgresql connection {name}"


assert test_database_registry["sqlite"]("quera") == f"sqlite connection quera"
assert test_database_registry["postgresql"]("quera") == f"postgresql connection quera"

"""
### Exceptions

{{exceptions}}

## Reference

Here is all the things you can do with the `Registerer` class:


{{Registerer}}

"""
