import inspect
import typing

from registerer.exceptions import (
    ItemAlreadyRegistered,
    ItemNotRegistered,
    RegistrationError,
)
from registerer.validators import RegistryValidator

Type = typing.TypeVar("Type")


class Registerer(typing.Generic[Type]):
    """A utility that can be used to create a registry object to register class or functions."""

    registry_dict: typing.Dict[str, Type] = None
    parent_item: typing.Optional[typing.Type[Type]] = None
    max_size: typing.Optional[int] = None
    validators: typing.Optional[typing.List] = None

    def __init__(
        self,
        parent_item: typing.Optional[typing.Type[Type]] = None,
        *,
        max_size: int = None,
        validators: typing.Optional[typing.List] = None,
    ):
        """
        Args:
            parent_item: The class of parent. Defaults to None.
            max_size: allowed size of registered items. Defaults to None.
            validators: validate each item on register. Defaults to None.
        """
        self.registry_dict = {}
        self.parent_item = parent_item if parent_item else self.parent_item
        self.max_size = max_size
        self.validators = (validators if validators else []) + (self.validators if self.validators else [])

        for validator in self.validators:
            if not isinstance(validator, RegistryValidator):
                raise RegistrationError("the validator items should be objects of RegistryValidator or it's children.")

    @property
    def items(self) -> typing.Any:
        """
        get actual registered items (classes or functions)
        """
        for item in self.registry_dict.values():
            yield item

    def is_registered(self, slug: str) -> bool:
        """
        is the slug registered?
        """
        return slug in self.registry_dict

    def __getitem__(self, registry_slug: str) -> Type:
        """
        get the registered item by slug
        """
        try:
            return self.registry_dict[registry_slug]
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    def validate(self, item: Type):
        """validate the item during registration.

        Args:
            item (Type): item want to register.

        Raises:
            RegistrationError: can't register this item.
        """
        if self.parent_item is not None and inspect.isclass(item) and not issubclass(item, self.parent_item):
            raise RegistrationError(f"'{item.__name__}' class should be a subclass of '{self.parent_item.__name__}'.")

        if inspect.isclass(item) and issubclass(item, Registerer):
            raise RegistrationError(f"Don't register a class inherited from Registerer. It's anti-pattern.")

        if self.max_size is not None and len(self.registry_dict) >= self.max_size:
            raise RegistrationError(f"You can't register more than {self.max_size} items to this registry.")

        for validator in self.validators:
            validator(item)

    def __register(self, custom_slug: str = None, **kwargs):
        """the inner function that handles register

        Args:
            custom_slug (str): the unique identifier for the item.

        Raises:
            ItemAlreadyRegistered: There is another item already registered with this slug.
            RegistrationError: can't register this item.
        """

        def _wrapper_function(item: Type):
            registry_slug = custom_slug if custom_slug else item.__name__

            if self.is_registered(registry_slug):
                raise ItemAlreadyRegistered(f"There is another item already registered with slug='{registry_slug}'.")

            item.registry_slug = registry_slug
            for key, value in kwargs.items():
                setattr(item, key, value)

            self.validate(item)

            self.registry_dict[registry_slug] = item
            return item

        return _wrapper_function

    def register(self, *args, **kwargs):
        """register a class or item to the registry
        example:

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

        """
        if len(args) == 1 and kwargs == {} and (inspect.isfunction(args[0]) or inspect.isclass(args[0])):
            # register function is not called
            return self.__register()(args[0])

        if len(args) == 0 and kwargs == {}:
            # unnecessary call
            raise RegistrationError(
                "Pass the registry_slug as positional argument"
                "or just don't call the register function to use the name of item."
            )

        return self.__register(*args, **kwargs)

    def __repr__(self) -> str:
        parent = f"{self.parent_item.__name__}" if self.parent_item else ""
        count = f"count={len(self.registry_dict)}"
        return f"<{parent}Registry {count}>"
