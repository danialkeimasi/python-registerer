import unittest

from registerer import (
    ItemNotRegistered,
    Registerer,
    RegistrationError,
    RegistryCreationError,
)


class Test(unittest.TestCase):
    def test_not_registered(self):
        registry = Registerer()

        with self.assertRaises(ItemNotRegistered):
            registry["foo"]

    def test_register_duplicate(self):
        registry = Registerer()

        @registry.register()
        def foo():
            pass

        with self.assertRaises(RegistrationError):

            @registry.register("foo")
            def foo2():
                pass

    def test_function_register(self):
        registry = Registerer()

        @registry.register()
        def foo():
            return "bar"

        self.assertTrue(registry._registry_dict == {"foo": foo})
        self.assertTrue(list(registry.items) == [foo])
        self.assertTrue(registry.is_registered("foo"))
        self.assertTrue(registry["foo"]() == "bar")

    def test_class_register(self):
        class Parent:
            pass

        registry = Registerer(Parent)

        @registry.register("child")
        class Child(Parent):
            pass

        with self.assertRaises(RegistrationError):

            @registry.register("unrelated")
            class Unrelated:
                pass

        self.assertTrue(registry._registry_dict == {"child": Child})
        self.assertTrue(registry.is_registered("child"))
        self.assertTrue(not registry.is_registered("unrelated"))

        instance = registry["child"]()
        self.assertTrue(isinstance(instance, Child))
        self.assertTrue(isinstance(instance, Parent))

    def test_max_size(self):
        registry = Registerer(max_size=1)

        @registry.register()
        def foo():
            pass

        with self.assertRaises(RegistrationError):

            @registry.register()
            def foo():
                pass

        with self.assertRaises(RegistrationError):

            @registry.register()
            def foo2():
                pass

    def test_avoid_registering_registerer(self):
        class Parent(Registerer):
            pass

        registry = Registerer(Parent)

        with self.assertRaises(RegistrationError):

            @registry.register()
            class Child(Parent):
                pass

    def test_constructor(self):

        with self.assertRaises(RegistryCreationError):
            Registerer(validators=[lambda item: True])

        with self.assertRaises(RegistryCreationError):
            Registerer(max_size=0)

        with self.assertRaises(RegistryCreationError):
            Registerer(max_size=0.2)

    def test_function_attribute_setter(self):
        registry = Registerer()

        @registry.register(branch="test")
        def test():
            pass

        @registry.register("prod", branch="prod")
        def postgres_prod():
            pass

        self.assertTrue(test.branch == "test")
        self.assertTrue(registry["test"].branch == "test")
        self.assertTrue(postgres_prod.branch == "prod")
        self.assertTrue(registry["prod"].branch == "prod")


if __name__ == "__main__":
    unittest.main()
