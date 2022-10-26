import inspect
import typing

from registerer.exceptions import (
    ItemNotRegistered,
    RegistrationError,
    RegistryCreationError,
)
from registerer.validators import RegistryValidator

T = typing.TypeVar("T")


class Registerer(typing.Generic[T]):
    """A utility that can be used to create a registry object to register class or functions."""

    _registry_dict: typing.Dict[str, T] = None
    parent_class: typing.Optional[T] = None
    max_size: typing.Optional[int] = None
    validators: typing.Optional[typing.List] = None

    def __init__(
        self,
        parent_class: typing.Optional[T] = None,
        *,
        max_size: typing.Optional[int] = None,
        validators: typing.Optional[typing.List[RegistryValidator]] = None,
    ):
        """
        Args:
            parent_class: The class of parent.
                If you set this, the registered class should be subclass of the this,
                If it's not the register method going to raise RegistrationError.
                Also by setting this you'll be benefit from type hints in your IDE.
            max_size: allowed size of registered items.
                Defaults to None which means there is no limit.
            validators: custom validation for on registering items.

        Raises:
            RegistryCreationError: Can't create proper registry object.
        """
        self._registry_dict = {}
        self.parent_class = parent_class if parent_class else self.parent_class
        self.max_size = max_size
        self.validators = (validators if validators else []) + (self.validators if self.validators else [])

        if self.max_size is not None and (not isinstance(self.max_size, int) or self.max_size <= 0):
            raise RegistryCreationError("max_size should be a int bigger than zero or None.")

        for validator in self.validators:
            if not isinstance(validator, RegistryValidator):
                raise RegistryCreationError("validator items should be function or object of RegistryValidator.")

    @property
    def items(self) -> typing.List[T]:
        """
        get actual registered items as list (classes or functions)
        """
        return list(self._registry_dict.values())

    def is_registered(self, slug: str) -> bool:
        """
        is the slug registered?
        """
        return slug in self._registry_dict

    def __getitem__(self, registry_slug: str) -> T:
        """
        get the registered item by slug
        """
        try:
            return self._registry_dict[registry_slug]
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    def validate(self, item: T):
        """validate the item during registration.

        Args:
            item (T): item want to register.

        Raises:
            RegistrationError: can't register this item.
        """
        if self.parent_class is not None and inspect.isclass(item) and not issubclass(item, self.parent_class):
            raise RegistrationError(f"'{item.__name__}' class should be a subclass of '{self.parent_class.__name__}'.")

        if inspect.isclass(item) and issubclass(item, Registerer):
            raise RegistrationError(f"Don't register a class inherited from Registerer. It's anti-pattern.")

        if self.max_size is not None and len(self._registry_dict) >= self.max_size:
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

        def _wrapper_function(item: T):
            registry_slug = custom_slug if custom_slug else item.__name__

            if self.is_registered(registry_slug):
                raise RegistrationError(f"There is another item already registered with slug='{registry_slug}'.")

            item.registry_slug = registry_slug
            for key, value in kwargs.items():
                setattr(item, key, value)

            self.validate(item)

            self._registry_dict[registry_slug] = item
            return item

        return _wrapper_function

    def register(self, item_or_custom_slug: typing.Union[T, str] = None, **kwargs):
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
        if item_or_custom_slug is not None and kwargs == {} and not isinstance(item_or_custom_slug, str):
            # register function is not called,
            # and item_or_custom_slug is a item (function or class).
            return self.__register()(item_or_custom_slug)

        if item_or_custom_slug is None and kwargs == {}:
            # unnecessary call
            raise RegistrationError(
                "Pass the registry_slug as positional argument"
                "or just don't call the register function to use the name of item."
            )

        # item_or_custom_slug is a custom_slug
        return self.__register(item_or_custom_slug, **kwargs)

    def __repr__(self) -> str:
        parent = f"{self.parent_class.__name__}" if self.parent_class else ""
        count = f"count={len(self._registry_dict)}"
        return f"<{parent}Registry {count}>"
