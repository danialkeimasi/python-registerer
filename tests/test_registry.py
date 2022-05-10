import unittest

from registerer.registry import (
    Registerer,
    ItemAlreadyRegistered,
    ItemNotRegistered,
)


class Test(unittest.TestCase):
    def test_not_registered(self):
        registry = Registerer()

        with self.assertRaises(ItemNotRegistered):
            registry.get("foo")

    def test_register_duplicate(self):
        registry = Registerer()

        @registry.register("foo")
        def foo():
            return "bar"

        with self.assertRaises(ItemAlreadyRegistered):

            @registry.register("foo")
            def foo2():
                return "bar2"

    def test_immutable_registry_dict(self):
        registry = Registerer()
        registry.registry_dict["foo"] = "bar"
        self.assertTrue(not registry.is_registered("foo"))

    def test_function_register(self):
        registry = Registerer()

        @registry.register("foo")
        def foo():
            return "bar"

        self.assertTrue(registry.registry_dict == {"foo": foo})
        self.assertTrue(registry.is_registered("foo"))
        self.assertTrue(registry.get("foo")() == "bar")

    def test_class_register(self):
        class Parent:
            pass

        registry = Registerer(Parent)

        @registry.register("child")
        class Child(Parent):
            pass

        with self.assertRaises(TypeError):

            @registry.register("unrelated")
            class Unrelated:
                pass

        self.assertTrue(registry.registry_dict == {"child": Child})
        self.assertTrue(registry.is_registered("child"))
        self.assertTrue(not registry.is_registered("unrelated"))

        instance = registry.get("child")()
        self.assertTrue(isinstance(instance, Child))
        self.assertTrue(isinstance(instance, Parent))


if __name__ == "__main__":
    unittest.main()
