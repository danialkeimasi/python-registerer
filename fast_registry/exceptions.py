class RegistrationError(Exception):
    pass


class ItemAlreadyRegistered(RegistrationError):
    pass


class ItemNotRegistered(RegistrationError):
    pass
