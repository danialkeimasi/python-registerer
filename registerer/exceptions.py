class RegistryCreationError(Exception):
    """Errors that occurs on creating a registry object."""

    pass


class RegistrationError(Exception):
    """Errors that occurs on registering new item."""

    pass


class ItemNotRegistered(Exception):
    """You've tried to get a item that is not registered."""

    pass
