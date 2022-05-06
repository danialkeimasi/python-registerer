import unittest

from fast_registry import FastRegistry, RegistrationError, RegistryValidator
from fast_registry.validators import FunctionAnnotationValidator


class TestFastRegistry(unittest.TestCase):
    def test_validator(self):
        class MyRegistryValidator(RegistryValidator):
            def on_register(self, slug, item, registry_dict):
                raise RegistrationError(
                    f"{item.__name__}.size should be small or large."
                )

        registry = FastRegistry(validators=[MyRegistryValidator()])

        with self.assertRaises(RegistrationError):

            @registry.register("foo")
            class Foo:
                pass

    def test_function_annotations_validator(self):
        registry = FastRegistry(
            validators=[
                FunctionAnnotationValidator(annotations=[("name", str)]),
            ]
        )

        @registry.register("foo")
        def foo(name: str):
            pass

        with self.assertRaises(RegistrationError):

            @registry.register("bar")
            def bar(name_fa: str):
                pass


if __name__ == "__main__":
    unittest.main()
