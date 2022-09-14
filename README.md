# Registerer
[![](https://img.shields.io/pypi/v/registerer.svg)](https://pypi.python.org/pypi/registerer/)
[![](https://github.com/danialkeimasi/python-registerer/workflows/tests/badge.svg)](https://github.com/danialkeimasi/python-registerer/actions)
[![](https://img.shields.io/github/license/danialkeimasi/python-registerer.svg)](https://github.com/danialkeimasi/python-registerer/blob/master/LICENSE)

Everything you need to implement maintainable and easy to use registry patterns in your project.
# Installation

```sh
pip install registerer
```


## Examples

### Register a Function With Validator

```python
import registerer

database_registry = registerer.Registerer(
    validators=[registerer.RegistryValidator(lambda item: not getattr(item, "fail", False))]
)

# success:
@database_registry.register("sqlite")
def sqlite_database_connection(name: str):
    return f"sqlite connection {name}"


# failure:
# registerer.exceptions.RegistrationError: custom validation failed when registering postgres_database_connection
@database_registry.register("postgres", fail=True)
def postgres_database_connection(name: str):
    return f"postgres connection {name}"


def main():
    print(database_registry["postgres"]("personal"))  # postgres connection personal


if __name__ == "__main__":
    main()

```

### Register a Function

```python
# Register functions:

from registerer import Registerer

database_registry = Registerer()


@database_registry.register
def sqlite():
    return "sqlite connection"


@database_registry.register("postgres")
def postgres_backup():
    return "postgres connection"


def main():
    print(database_registry["sqlite"]())  # sqlite connection
    print(database_registry["postgres"]())  # postgres connection


if __name__ == "__main__":
    main()

```

### Register a Class With Custom Validator

```python
import registerer


class Animal:
    is_wild: bool = None


domestic_animals_registry = registerer.Registerer(
    Animal,
    max_size=4,
    validators=[
        registerer.RegistryValidator(
            lambda item: not item.is_wild,
            error="only domestic animals allowed.",  # Optional
        ),
    ],
)


# success:
@domestic_animals_registry.register("cow")
class Cow(Animal):
    is_wild = False


# failure:
# raises registerer.exceptions.RegistrationError: Lion is wild, only domestic animals are allowed to register.
@domestic_animals_registry.register("lion")
class Lion(Animal):
    is_wild = True

```

### Register a Class

```python
# Register classes with the same interface,
# enforce the type check and enjoy the benefits of type hints:


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


def main():
    print(animal_registry["dog"])  # <class '__main__.Dog'>
    print(animal_registry["dog"]())  # <__main__.Dog object at 0x7f108ad37d60>
    print(animal_registry["dog"]().talk())  # woof


if __name__ == "__main__":
    main()

```

## Reference


### <kbd>module</kbd> `registerer.registry`






---

#### <kbd>class</kbd> `Registerer`
A utility that can be used to create a registry object to register class or functions. 

### <kbd>method</kbd> `Registerer.__init__`

```python
__init__(
    parent_item: Optional[Type[~Type]] = None,
    max_size: int = None,
    validators: Optional[List] = None
)
```



**Args:**
 
 - <b>`parent_item`</b>:  The class of parent. Defaults to None. 
 - <b>`max_size`</b>:  allowed size of registered items. Defaults to None. 
 - <b>`validators`</b>:  validate each item on register. Defaults to None. 


---

###### <kbd>property</kbd> Registerer.items

get actual registered items (classes or functions) 



---

##### <kbd>method</kbd> `Registerer.is_registered`

```python
is_registered(slug: str) → bool
```

is the slug registered? 

---

##### <kbd>method</kbd> `Registerer.register`

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

##### <kbd>method</kbd> `Registerer.validate`

```python
validate(item: ~Type)
```

validate the item during registration. 



**Args:**
 
 - <b>`item`</b> (Type):  item want to register. 



**Raises:**
 
 - <b>`RegistrationError`</b>:  can't register this item. 






### <kbd>module</kbd> `registerer.validators`






---

#### <kbd>class</kbd> `RegistryValidator`
a utility for custom validation with the Registerer. you can subclass this and override the on_register method, and raise an exception if you must. 



**examples:**
 

```python


### <kbd>method</kbd> `RegistryValidator.__init__`

```python
__init__(validator, error: str = None) → None
```













### <kbd>module</kbd> `registerer.exceptions`






---

#### <kbd>class</kbd> `RegistrationError`
Errors that occurs on registering new item. 





---

#### <kbd>class</kbd> `ItemAlreadyRegistered`
You've registered a item with duplicate identifier. 





---

#### <kbd>class</kbd> `ItemNotRegistered`
You've tried to get a item that is not registered. 







