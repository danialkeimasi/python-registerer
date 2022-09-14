import unittest

from registerer.exceptions import RegistrationError
from registerer.registry import ItemAlreadyRegistered, ItemNotRegistered, Registerer


class Test(unittest.TestCase):
    def test_not_registered(self):
        registry = Registerer()

        with self.assertRaises(ItemNotRegistered):
            registry["foo"]

    def test_register_duplicate(self):
        registry = Registerer()

        @registry.register
        def foo():
            return "bar"

        with self.assertRaises(ItemAlreadyRegistered):

            @registry.register("foo")
            def foo2():
                return "bar2"

    def test_function_register(self):
        registry = Registerer()

        @registry.register
        def foo():
            return "bar"

        self.assertTrue(registry.registry_dict == {"foo": foo})
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

        self.assertTrue(registry.registry_dict == {"child": Child})
        self.assertTrue(registry.is_registered("child"))
        self.assertTrue(not registry.is_registered("unrelated"))

        instance = registry["child"]()
        self.assertTrue(isinstance(instance, Child))
        self.assertTrue(isinstance(instance, Parent))


if __name__ == "__main__":
    unittest.main()
