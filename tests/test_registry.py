import pytest

from registerer import ItemNotRegistered, Registerer, RegistrationError, RegistryCreationError


def test_not_registered():
    registry = Registerer()

    with pytest.raises(ItemNotRegistered):
        registry["foo"]


def test_register_duplicate():
    registry = Registerer()

    @registry.register()
    def foo():
        pass

    with pytest.raises(RegistrationError):

        @registry.register("foo")
        def foo2():
            pass


def test_function_register():
    registry = Registerer()

    @registry.register()
    def foo():
        return "bar"

    assert registry._registry_dict == {"foo": foo}
    assert list(registry.items) == [foo]
    assert registry.is_registered("foo")
    assert registry["foo"]() == "bar"


def test_class_register():
    class Parent:
        pass

    registry = Registerer(Parent)

    @registry.register("child")
    class Child(Parent):
        pass

    with pytest.raises(RegistrationError):

        @registry.register("unrelated")
        class Unrelated:
            pass

    assert registry._registry_dict == {"child": Child}
    assert registry.is_registered("child")
    assert not registry.is_registered("unrelated")

    instance = registry["child"]()
    assert isinstance(instance, Child)
    assert isinstance(instance, Parent)


def test_max_size():
    registry = Registerer(max_size=1)

    @registry.register()
    def foo():
        pass

    with pytest.raises(RegistrationError):

        @registry.register()
        def foo():
            pass

    with pytest.raises(RegistrationError):

        @registry.register()
        def foo2():
            pass


def test_avoid_registering_registerer():
    class Parent(Registerer):
        pass

    registry = Registerer(Parent)

    with pytest.raises(RegistrationError):

        @registry.register()
        class Child(Parent):
            pass


def test_constructor():

    with pytest.raises(RegistryCreationError):
        Registerer(validators=[lambda item: True])  # type: ignore

    with pytest.raises(RegistryCreationError):
        Registerer(max_size=0)

    with pytest.raises(RegistryCreationError):
        Registerer(max_size=0.2)  # type: ignore


def test_function_attribute_setter():
    registry = Registerer()

    @registry.register(branch="test")
    def test():
        pass

    @registry.register("prod", branch="prod")
    def postgres_prod():
        pass

    assert test.branch == "test"
    assert registry["test"].branch == "test"
    assert postgres_prod.branch == "prod"
    assert registry["prod"].branch == "prod"
