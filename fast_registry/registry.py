import typing

Type = typing.TypeVar("Type")


class ItemAlreadyRegistered(Exception):
    pass


class ItemNotRegistered(Exception):
    pass


class FastRegistry(typing.Generic[Type]):
    """
    A generic class that can be used to register classes or functions.
    With type hints support.

    - example
    ```
        class Animal:
            def talk(self):
                raise NotImplementedError

        # create a registry that requires registered items to implement the Animal interface.
        animal_registry = FastRegistry(Animal)

        @animal_registry("dog")
        class Dog:
            def talk(self):
                return "woof"

        >> animal_registry["dog"]
        <class '__main__.Dog'>

        >> animal_registry["dog"]()
        <__main__.Dog object at 0x7fda96d3b310>

        >> animal_registry["dog"]().talk()
        'woof'
    ```
    """

    _registry = {}

    def __init__(self, item_type: typing.Optional[Type] = None):
        pass

    def is_registered(self, slug: str) -> bool:
        """
        is the slug registered?
        """
        return slug in self._registry

    def __contains__(self, slug: str) -> bool:
        return self.is_registered(slug)

    def __getitem__(self, slug: str) -> Type:
        if slug not in self._registry:
            raise ItemNotRegistered(f"The {slug} is not registered")
        return self._registry[slug]

    def __call__(self, slug: str):
        """
        register a new function or class
        """

        def _wrapper_function(item):
            item.slug = slug
            self._registry[slug] = item
            return item

        if self.is_registered(slug):
            raise ItemAlreadyRegistered(f"There is another item with slug='{slug}'.")

        return _wrapper_function
