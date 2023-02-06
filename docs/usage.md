# Usage

## Installation

You can install the latest version of registerer from PyPI:

```sh
pip install registerer
```

## Usage

In order to use registerer, you need to instantiate from the `registerer.Registerer`.

There is several optional arguments you can pass to the `Registerer` constructor
to manage how registry object should behave (Read more in reference section).

### Registering Classes

```python exec="true" source="above"
import registerer


class Animal:
    slug: str
    is_wild: bool

    def walk(self):
        pass


animal_registry = registerer.Registerer(

    # the registered item will only be sub-class of Animal.
    # this argument is necessary for type hints.
    parent_class=Animal,

    # only 5 items can be registered.
    max_size=5,

    # - set the slug of item as attribute on it.
    # - and also use the value of this attribute as slug if no
    #   custom_slug passed to register method on registration.
    slug_attr="slug",

    validators=[
        registerer.RegistryValidator(
            lambda item: item.is_wild is False,  # check passed if returns True
            error="can't register wild animal.",
        ),
    ],
)

# Now with `animal_registry` you can register your classes:

# use the name of class as unique identifier:
@animal_registry.register()
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


assert animal_registry["kitty"] == Cat
assert animal_registry["Sheep"]().walk() == "sheep walks"

assert animal_registry.items == [Sheep, Cat]
assert Cat.slug == animal_registry["kitty"].slug == "kitty"

# use this for django choices, etc.
assert (
    animal_registry.attrs_as_tuples("slug", "__name__") ==
    [('Sheep', 'Sheep'), ('kitty', 'Cat')]
)

```

### Registering Functions

if you need to add attributes on the registered item on registration (it's optional),
you can pass kwargs to the `register` method.

This is useful when registering functions. for example:

```python exec="true" source="above"
import registerer

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

## Notes

### The Slug Attribute

The value of `slug_attr` passed to the Registerer is the name of a special attribute. As you know each item has it's unique identifier.
Registerer will sync the registry identifier with this given attribute.

When you are registering an item, the identifier slug could be on of these values (In order of preference):

- Custom slug: given to `registry.register` method as first positional argument.
- The value of given attribute by `slug_attr`.
- The name of item (`__name__`).

### Choices For Django

You may need to map the registered items to an object on Database. Having the items as choices on model field will help you with building admin and form choices.

If you need to create choices for your model field, use `registry.attrs_as_tuples` method.

For example:

```python

class EventStep(models.Model):
    _step_slug = models.CharField(
        choices=registry.attrs_as_tuples("slug", "name"), max_length=100
    )

```
