import unittest

from registerer import Registerer, RegistrationError, RegistryValidator


class Test(unittest.TestCase):
    def test_validator(self):

        registry = Registerer(
            slug_attr="slug",
            validators=[
                RegistryValidator(
                    lambda item: item.slug != "no",
                    error="oh no, registered class is not ok!",
                ),
            ],
        )

        @registry.register()
        class Foo:
            pass

        with self.assertRaises(RegistrationError):

            @registry.register("no")
            class Foo2:
                pass


if __name__ == "__main__":
    unittest.main()
