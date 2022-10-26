import typing

from registerer.exceptions import RegistrationError


class RegistryValidator:
    """
    a utility for custom validation with the Registerer.
    you can subclass this and override the on_register method, and raise an exception if you must.

    """

    def __init__(self, validator, *, error: typing.Optional[str] = None) -> None:
        self.validator = validator
        self.error = error

    def __call__(self, item):
        """
        this function will be called when registering an item

        args:
            item (Any): the item that is being registered (the class or function)
        """
        if not self.validator(item):
            raise RegistrationError(
                self.error if self.error else f"custom validation failed when registering {item.__name__}"
            )
