import typing

from fast_registry.exceptions import RegistrationError


class RegistryValidator:
    """
    a utility for custom validation with the FastRegistry.
    you can subclass this and override the on_register method, and raise an exception if you must.
    """

    def on_register(self, slug: str, item, registry_dict: typing.Dict[str, typing.Any]):
        """
        this function will be called when registering an item

        args:
            slug (str): the slug or identifier of the item that is being registered
            item (Any): the item that is being registered (the class or function)
            registry_dict (Dict[str, Any]): dictionary containing all the items that are registered so far
        """
        raise NotImplementedError


class FunctionAnnotationValidator(RegistryValidator):
    """
    use this validator to check annotations of registered functions
    """

    def __init__(self, annotations: typing.List[typing.Tuple[str, any]]) -> None:
        self.expected_annotations = annotations

    def on_register(self, slug: str, item, registry_dict: typing.Dict[str, typing.Any]):
        if self.expected_annotations and not getattr(item, "__annotations__", None):
            raise ValueError(
                f"function '{item.__name__}' does not have any type annotations."
            )

        function_annotations = list(item.__annotations__.items())
        if self.expected_annotations != function_annotations:
            raise RegistrationError(
                f"The '{item.__name__}' function with slug='{slug}' do not match the expected annotations.\n"
                f"Expected: {self.expected_annotations}\n"
                f"Got: {function_annotations}"
            )
