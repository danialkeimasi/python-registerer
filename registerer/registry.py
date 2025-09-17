import copy
import inspect
import sys
import typing
from collections.abc import Hashable

from registerer.exceptions import ItemNotRegistered, RegistrationError, RegistryCreationError
from registerer.validators import RegistryValidator

if sys.version_info >= (3, 13):  # PEP 696: default type parameter support
    K = typing.TypeVar("K", bound=Hashable, default=str)  # type: ignore[call-arg]
    T = typing.TypeVar("T", default=typing.Any)  # type: ignore[call-arg]
else:
    K = typing.TypeVar("K", bound=Hashable)
    T = typing.TypeVar("T")

# Default type for `get`'s fallback
S = typing.TypeVar("S")


class Registerer(typing.Generic[K, T]):
    """A utility that can be used to create a registry object to register class or functions."""

    def __init__(
        self,
        parent_class: typing.Optional[type[T]] = None,
        *,
        slug_attr: typing.Optional[str] = None,
        max_size: typing.Optional[int] = None,
        validators: typing.Optional[list[RegistryValidator]] = None,
    ):
        """
        Args:
            parent_class: The class of parent.
                If you set this, the registered class should be subclass of the this,
                If it's not the register method going to raise RegistrationError.
                Also by setting this you'll be benefit from type hints in your IDE.
            slug_attr: Pass the attribute name of registered item that you want to
                set registry slug to or read from registered item.
            max_size: allowed size of registered items.
                Defaults to None which means there is no limit.
            validators: custom validation for on registering items.

        Raises:
            RegistryCreationError: Can't create proper registry object.
        """
        self._registry_dict: dict[K, type[T]] = {}
        self.parent_class: typing.Optional[type[T]] = parent_class
        self.max_size: typing.Optional[int] = max_size
        self.slug_attr: typing.Optional[str] = slug_attr
        self.validators: list = validators if validators else []

        if self.max_size is not None and (not isinstance(self.max_size, int) or self.max_size <= 0):
            raise RegistryCreationError("max_size should be a int bigger than zero or None.")

        for validator in self.validators:
            if not isinstance(validator, RegistryValidator):
                raise RegistryCreationError("validator items should be object of RegistryValidator.")

    @property
    def items(self) -> list[type[T]]:
        """
        Get actual registered items as list (classes or functions)
        """
        return list(self._registry_dict.values())

    def is_registered(self, slug: K) -> bool:
        """
        Is the slug registered with any item?
        """
        return slug in self._registry_dict

    def __getitem__(self, registry_slug: K) -> type[T]:
        """
        get the registered item by slug
        """
        try:
            return self._registry_dict[registry_slug]
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    @typing.overload
    def get(self, registry_slug: K) -> typing.Optional[type[T]]: ...

    @typing.overload
    def get(self, registry_slug: K, default: S) -> typing.Union[type[T], S]: ...

    def get(self, registry_slug: K, default: typing.Optional[S] = None) -> typing.Union[type[T], S, None]:
        """
        Return the value for key if key is in the registry, else default.
        """
        return self._registry_dict.get(registry_slug, default)  # type: ignore[return-value]

    def validate(self, item: type[T]):
        """Validate the item during registration.

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

    def register(self, custom_slug: typing.Optional[K] = None, **kwargs):
        """Register a class or item to the registry
        example:

        ```python
        # register the item with it's name
        @registry.register()
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

        Args:
            custom_slug (K): the unique identifier for the item.

        Raises:
            ItemAlreadyRegistered: There is another item already registered with this slug.
            RegistrationError: can't register this item.
        """

        def _wrapper_function(item):
            # When no custom slug is provided, fall back to str-based slug.
            # For non-str key types, callers should always pass `custom_slug`.
            registry_slug: K = typing.cast(K, custom_slug or getattr(item, self.slug_attr or "", "") or item.__name__)

            if self.is_registered(registry_slug):
                raise RegistrationError(f"There is another item already registered with slug='{registry_slug}'.")

            if self.slug_attr:
                setattr(item, self.slug_attr, registry_slug)

            for key, value in kwargs.items():
                setattr(item, key, value)

            self.validate(item)

            self._registry_dict[registry_slug] = item
            return item

        return _wrapper_function

    def unregister(self, registry_slug: K) -> None:
        """
        Unregister the item with given slug.
        """
        try:
            self._registry_dict.pop(registry_slug)
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    def filter(self, function: typing.Callable[[type[T]], bool]) -> "Registerer[K, T]":
        """
        Filter the registry with given callback and create
        another subset registry with desired items in it.
        """
        registry = copy.deepcopy(self)
        registry._registry_dict = {slug: item for slug, item in registry._registry_dict.items() if function(item)}
        return registry

    def attrs_as_tuples(self, *args: str, flat: bool = False) -> list[tuple]:
        """
        Returns list of tuples of based on attributes of registered items.
        You can use this to create choices for Django model field.

        Inspired by values_list in Django's QuerySet.

        ```python
        registry = registerer.Registerer()

        @registry.register()
        class ContestStep:
            slug = "contest"
            name = "Contest"

        @registry.register()
        class CollegeStep:
            slug = "college"
            name = "College"

        assert registry.attrs_as_tuples("slug", "name") == [("contest", "Contest"), ("college", "College")]
        assert registry.attrs_as_tuples("slug", flat=True) == ["contest", "college"]

        class Step(django.db.models.Model):
            step_slug = models.CharField(max_length=100, choices=registry.attrs_as_tuples("slug", "name"))
        ```
        """
        if not args:
            raise ValueError("Select at least one attribute.")

        if len(args) > 1 and flat:
            raise ValueError("'flat' is not valid when attrs_as_tuples is called with more than one attribute.")

        if flat:
            return [getattr(item, args[0]) for item in self.items]

        return [tuple(getattr(item, field) for field in args) for item in self.items]

    def __repr__(self) -> str:
        parent = f"{self.parent_class.__name__}" if self.parent_class else ""
        count = f"count={len(self._registry_dict)}"
        return f"<{parent}Registry {count}>"
