import unittest

from registerer import Registerer, RegistrationError, RegistryValidator


class Test(unittest.TestCase):
    def test_validator(self):

        registry = Registerer(
            validators=[
                RegistryValidator(lambda item: item.registry_slug != "no"),
            ],
        )

        @registry.register
        class Foo:
            pass

        with self.assertRaises(RegistrationError):

            @registry.register("no")
            class Foo:
                pass


if __name__ == "__main__":
    unittest.main()
