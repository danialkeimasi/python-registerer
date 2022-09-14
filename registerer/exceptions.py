class RegistrationError(Exception):
    """Errors that occurs on registering new item."""

    pass


class ItemAlreadyRegistered(RegistrationError):
    """You've registered a item with duplicate identifier."""

    pass


class ItemNotRegistered(RegistrationError):
    """You've tried to get a item that is not registered."""

    pass
