class RegistryCreationError(Exception):
    """Errors that occurs on creating a registry object."""


class RegistrationError(Exception):
    """Errors that occurs on registering new item."""


class ItemNotRegistered(Exception):
    """You've tried to get a item that is not registered."""
