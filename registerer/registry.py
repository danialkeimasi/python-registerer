import copy
import inspect
import typing

from registerer.exceptions import ItemNotRegistered, RegistrationError, RegistryCreationError
from registerer.validators import RegistryValidator

T = typing.TypeVar("T")


class Registerer(typing.Generic[T]):
    """A utility that can be used to create a registry object to register class or functions."""

    def __init__(
        self,
        parent_class: typing.Optional[typing.Type[T]] = None,
        *,
        slug_attr: typing.Optional[str] = None,
        max_size: typing.Optional[int] = None,
        validators: typing.Optional[typing.List[RegistryValidator]] = None,
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
        self._registry_dict: typing.Dict[str, typing.Type[T]] = {}
        self.parent_class: typing.Optional[typing.Type[T]] = parent_class
        self.max_size: typing.Optional[int] = max_size
        self.slug_attr: typing.Optional[str] = slug_attr
        self.validators: typing.List = validators if validators else []

        if self.max_size is not None and (not isinstance(self.max_size, int) or self.max_size <= 0):
            raise RegistryCreationError("max_size should be a int bigger than zero or None.")

        for validator in self.validators:
            if not isinstance(validator, RegistryValidator):
                raise RegistryCreationError("validator items should be function or object of RegistryValidator.")

    @property
    def items(self) -> typing.List[typing.Type[T]]:
        """
        Get actual registered items as list (classes or functions)
        """
        return list(self._registry_dict.values())

    def is_registered(self, slug: str) -> bool:
        """
        Is the slug registered with any item?
        """
        return slug in self._registry_dict

    def __getitem__(self, registry_slug: str) -> typing.Type[T]:
        """
        get the registered item by slug
        """
        try:
            return self._registry_dict[registry_slug]
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    def get(self, registry_slug: str, default: typing.Optional[typing.Any] = None) -> typing.Optional[typing.Type[T]]:
        """
        Return the value for key if key is in the registry, else default.
        """
        return self._registry_dict.get(registry_slug, default)

    def validate(self, item: typing.Type[T]):
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

    def register(self, custom_slug: typing.Optional[str] = None, **kwargs):
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
            custom_slug (str): the unique identifier for the item.

        Raises:
            ItemAlreadyRegistered: There is another item already registered with this slug.
            RegistrationError: can't register this item.
        """

        def _wrapper_function(item):
            registry_slug = custom_slug or getattr(item, self.slug_attr or "", "") or item.__name__

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

    def unregister(self, registry_slug: str) -> None:
        """
        Unregister the item with given slug.
        """
        try:
            self._registry_dict.pop(registry_slug)
        except KeyError:
            raise ItemNotRegistered(f"The item with slug='{registry_slug}' is not registered.")

    def filter(self, function: typing.Callable[[typing.Type[T]], bool]) -> "Registerer":
        """
        Filter the registry with given callback and create
        another subset registry with desired items in it.
        """
        registry = copy.deepcopy(self)
        registry._registry_dict = {slug: item for slug, item in registry._registry_dict.items() if function(item)}
        return registry

    def attrs_as_tuples(self, *args: str, flat: bool = False) -> typing.List[typing.Tuple]:
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
