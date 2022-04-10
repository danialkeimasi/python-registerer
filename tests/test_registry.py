import unittest

from fast_registry.registry import (
    FastRegistry,
    ItemAlreadyRegistered,
    ItemNotRegistered,
)


class TestFastRegistry(unittest.TestCase):
    def test_not_registered(self):
        registry = FastRegistry()

        with self.assertRaises(ItemNotRegistered):
            registry["foo"]

    def test_register_duplicate(self):
        registry = FastRegistry()

        @registry("foo")
        def foo():
            return "bar"

        with self.assertRaises(ItemAlreadyRegistered):

            @registry("foo")
            def foo2():
                return "bar2"

    def test_immutable_registry_dict(self):
        registry = FastRegistry()
        registry.registry_dict["foo"] = "bar"
        self.assertTrue("foo" not in registry)

    def test_function_register(self):
        registry = FastRegistry()

        @registry("foo")
        def foo():
            return "bar"

        self.assertTrue(registry.registry_dict == {"foo": foo})
        self.assertTrue("foo" in registry)
        self.assertTrue(registry["foo"]() == "bar")

    def test_class_register(self):
        class Parent:
            pass

        registry = FastRegistry(Parent)

        @registry("child")
        class Child(Parent):
            pass

        with self.assertRaises(TypeError):

            @registry("unrelated")
            class Unrelated:
                pass

        self.assertTrue(registry.registry_dict == {"child": Child})
        self.assertTrue("child" in registry)
        self.assertTrue("unrelated" not in registry)

        instance = registry["child"]()
        self.assertTrue(isinstance(instance, Child))
        self.assertTrue(isinstance(instance, Parent))


if __name__ == "__main__":
    unittest.main()
