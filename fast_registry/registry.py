import typing


class ItemAlreadyRegistered(Exception):
    pass


class ItemNotRegistered(Exception):
    pass


Type = typing.TypeVar("Type")


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

    @property
    def registry_dict(self) -> typing.Dict[str, Type]:
        return self.__registry_dict.copy()

    def __init__(self, item_type: typing.Optional[Type] = None):
        self.__registry_dict: typing.Dict[str, Type] = {}
        self.__item_type = item_type

    def is_registered(self, slug: str) -> bool:
        """
        is the slug registered?
        """
        return slug in self.__registry_dict

    def __contains__(self, slug: str) -> bool:
        return self.is_registered(slug)

    def __getitem__(self, slug: str) -> Type:
        if slug not in self.__registry_dict:
            raise ItemNotRegistered(f"The {slug} is not registered")
        return self.__registry_dict[slug]

    def __call__(self, slug: str):
        """
        register a new function or class
        """
        if self.is_registered(slug):
            raise ItemAlreadyRegistered(f"There is another item with slug='{slug}'.")

        def _wrapper_function(item):
            if self.__item_type is not None and not issubclass(item, self.__item_type):
                raise TypeError(f"'{item.__name__}' class should be a subclass of '{self.__item_type.__name__}'")

            item.slug = slug
            self.__registry_dict[slug] = item
            return item

        return _wrapper_function
