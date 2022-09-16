# Registerer
[![pypi](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![ci](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![codecov](https://codecov.io/gh/danialkeimasi/python-registerer/branch/main/graph/badge.svg?token=Q5MG14RKJL)](https://codecov.io/gh/danialkeimasi/python-registerer)
[![license](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)


Implement maintainable and easy to use registry patterns in your project.

TLDR; Write this:
```python
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
```
Instead of this, which violates the Open-Closed Principle (OCP):
```python


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
```
## Installation

```sh
pip install registerer
```

## Usage

In order to use registerer, you need to instantiate from the `registerer.Registerer`.

There is several optional arguments you can pass to the `Registerer` constructor
to manage how registry object should behave (Read more in reference section).

let's create a registry:
```python

import abc


class Animal(abc.ABC):
    is_wild: bool = None

    @abc.abstractmethod
    def walk(self):
        pass


# Animal class registry
animal_registry = registerer.Registerer(
    parent_item=Animal,
    max_size=5,  # only 5 items can register
    validators=[
        registerer.RegistryValidator(
            lambda item: item.is_wild is False,  # check passed if returns True
            error="can't register wild animal.",
        ),
    ],
)


```
Now with `animal_registry` you can register your classes:
```python


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
assert animal_registry.registry_dict == {"sheep": Sheep, "kitty": Cat}

assert animal_registry["Sheep"]().walk() == "sheep walks"
assert animal_registry["kitty"]().walk() == "cat walks"
```
The `register` method will also set an attribute on the registered item as `registry_slug`.  
So, in last example we have:

```python
assert Cat.registry_slug == "kitty"
assert animal_registry["kitty"].registry_slug == "kitty"

```
if you need to add attributes on the registered item on registration (it's optional), you can pass kwargs to the `register` method.  
This is useful when registering functions. for example:
```python

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

```
### Exceptions


<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/exceptions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

#### <kbd>module</kbd> `registerer.exceptions`






---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/exceptions.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

##### <kbd>class</kbd> `RegistryCreationError`
Errors that occurs on creating a registry object. 





---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/exceptions.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

##### <kbd>class</kbd> `RegistrationError`
Errors that occurs on registering new item. 





---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/exceptions.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

##### <kbd>class</kbd> `ItemNotRegistered`
You've tried to get a item that is not registered. 







## Reference

Here is all the things you can do with the `Registerer` class:



<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/registry.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>class</kbd> `Registerer`
A utility that can be used to create a registry object to register class or functions. 

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/registry.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Registerer.__init__`

```python
__init__(
    parent_item: Optional[~T] = None,
    max_size: Optional[int] = None,
    validators: Optional[List[registerer.validators.RegistryValidator]] = None
)
```



**Args:**
 
 - <b>`parent_item`</b>:  The class of parent.  If you set this, the registered class should be subclass of the this,  If it's not the register method going to raise RegistrationError.  Also by setting this you'll be benefit from type hints in your IDE. 
 - <b>`max_size`</b>:  allowed size of registered items.  Defaults to None which means there is no limit. 
 - <b>`validators`</b>:  custom validation for on registering items. 



**Raises:**
 
 - <b>`RegistryCreationError`</b>:  Can't create proper registry object. 


---

##### <kbd>property</kbd> Registerer.items

get actual registered items as list (classes or functions) 



---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/registry.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

#### <kbd>method</kbd> `Registerer.is_registered`

```python
is_registered(slug: str) → bool
```

is the slug registered? 

---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/registry.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

#### <kbd>method</kbd> `Registerer.register`

```python
register(*args, **kwargs)
```

register a class or item to the registry 

**example:**
 

```python
# register the item with it's name
@registry.register
class Foo:
     pass

assert registry["Foo"] == Foo


# register the item with a custom name
@registry.register("bar")
class Bar:
     pass

assert registry["bar"] == Bar


# register the item with a custom name and also add some other attributes to it.
# it is more useful when registering functions.
@db_registry.register("postgresql", env="prod")
def postgresql_connection:
     pass

assert registry["postgresql"] == postgresql_connection
assert postgresql_connection.env == "prod"

``` 

---

<a href="https://github.com/danialkeimasi/python-registerer/tree/main/registerer/registry.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

#### <kbd>method</kbd> `Registerer.validate`

```python
validate(item: ~T)
```

validate the item during registration. 



**Args:**
 
 - <b>`item`</b> (T):  item want to register. 



**Raises:**
 
 - <b>`RegistrationError`</b>:  can't register this item. 



