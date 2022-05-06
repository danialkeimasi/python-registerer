import typing

from fast_registry.exceptions import (
    ItemAlreadyRegistered,
    ItemNotRegistered,
    RegistrationError,
)
from fast_registry.validators import RegistryValidator

Type = typing.TypeVar("Type")


class FastRegistry(typing.Generic[Type]):
    """
    A generic class that can be used to create a registrey object to register class or functions.
    With type hints support.
    """

    __registry_dict: typing.Dict[str, Type] = {}
    __item_type: typing.Optional[Type]
    __validators: typing.List[RegistryValidator] = []

    def __init__(
        self,
        item_type: typing.Optional[Type] = None,
        validators: typing.Optional[typing.List[RegistryValidator]] = None,
    ):
        self.__registry_dict: typing.Dict[str, Type] = {}
        self.__item_type = item_type
        self.__validators = [] if validators is None else validators

        for validator in self.__validators:
            if not isinstance(validator, RegistryValidator):
                raise RegistrationError(
                    "the validator items should be objects of RegistryValidator or it's children."
                )

    @property
    def registry_dict(self) -> typing.Dict[str, Type]:
        """
        get a copy of the registry dict
        """
        return self.__registry_dict.copy()

    def is_registered(self, slug: str) -> bool:
        """
        is the slug registered?
        """
        return slug in self.__registry_dict

    def get(self, slug: str) -> Type:
        """
        get the registered item by slug
        """
        if not self.is_registered(slug):
            raise ItemNotRegistered(f"The item with slug='{slug}' is not registered.")
        return self.__registry_dict[slug]

    def register(self, slug: str):
        """
        register a new function or class
        """
        if self.is_registered(slug):
            raise ItemAlreadyRegistered(
                f"There is another item already registered with slug='{slug}'."
            )

        def _wrapper_function(item: Type):
            if self.__item_type is not None and not issubclass(item, self.__item_type):
                raise TypeError(
                    f"'{item.__name__}' class should be a subclass of '{self.__item_type.__name__}'."
                )

            for validator in self.__validators:
                validator.on_register(slug, item, self.__registry_dict)

            item.slug = slug
            self.__registry_dict[slug] = item
            return item

        return _wrapper_function
