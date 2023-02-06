import pytest

from registerer import ItemNotRegistered, Registerer, RegistrationError, RegistryCreationError


def test_not_registered(simple_registry: Registerer):
    with pytest.raises(ItemNotRegistered):
        simple_registry["foo"]


def test_register_duplicate(simple_registry: Registerer, function):
    simple_registry.register("foo")(function)

    with pytest.raises(RegistrationError):
        simple_registry.register("foo")(function)


def test_function_register(simple_registry: Registerer, function):
    simple_registry.register("foo")(function)

    assert simple_registry._registry_dict == {"foo": function}
    assert simple_registry.items == [function]
    assert simple_registry.is_registered("foo")

    assert simple_registry["foo"] == function
    assert simple_registry.get("foo") == function
    assert simple_registry.get("not_found") is None
    assert simple_registry.get("not_found", "default") == "default"


def test_class_register(parent_registry: Registerer, Child, Parent):
    parent_registry.register("child")(Child)

    with pytest.raises(RegistrationError):
        parent_registry.register("unrelated")(type("UnrelatedClass", (), {}))

    assert parent_registry._registry_dict == {"child": Child}
    assert parent_registry.is_registered("child")
    assert not parent_registry.is_registered("unrelated")

    instance = parent_registry["child"]()
    assert isinstance(instance, Child)
    assert isinstance(instance, Parent)


def test_max_size(function):
    registry = Registerer(max_size=1)
    registry.register("foo")(function)

    with pytest.raises(RegistrationError):
        registry.register("foo")(function)

    with pytest.raises(RegistrationError):
        registry.register("foo2")(function)


def test_avoid_registering_registerer():
    class ParentRegisterer(Registerer):
        pass

    registry = Registerer(ParentRegisterer)

    with pytest.raises(RegistrationError):
        registry.register()(type("Child", (ParentRegisterer,), {}))


def test_constructor():

    with pytest.raises(RegistryCreationError):
        Registerer(validators=[lambda item: True])  # type: ignore

    with pytest.raises(RegistryCreationError):
        Registerer(max_size=0)

    with pytest.raises(RegistryCreationError):
        Registerer(max_size=0.2)  # type: ignore


def test_function_attribute_setter(simple_registry: Registerer):
    @simple_registry.register("test_db", branch="test")
    def postgres_test():
        pass

    @simple_registry.register("prod_db", branch="prod")
    def postgres_prod():
        pass

    assert postgres_test.branch == simple_registry["test_db"].branch == "test"
    assert postgres_prod.branch == simple_registry["prod_db"].branch == "prod"

    assert simple_registry.filter(lambda f: False).items == []
    assert simple_registry.filter(lambda f: True).items == simple_registry.items

    assert simple_registry.attrs_as_tuples("slug", "branch") == [("test_db", "test"), ("prod_db", "prod")]
    assert simple_registry.attrs_as_tuples("slug") == [("test_db",), ("prod_db",)]
    assert simple_registry.attrs_as_tuples("slug", flat=True) == ["test_db", "prod_db"]

    with pytest.raises(ValueError):
        simple_registry.attrs_as_tuples("slug", "branch", flat=True)

    with pytest.raises(ValueError):
        simple_registry.attrs_as_tuples()


def test_unregister(simple_registry: Registerer, function):
    simple_registry.register("foo")(function)
    assert simple_registry.is_registered("foo")

    simple_registry.unregister("foo")
    assert not simple_registry.is_registered("foo")

    with pytest.raises(ItemNotRegistered):
        simple_registry.unregister("not_found")


def test_register_from_name(simple_registry: Registerer):
    @simple_registry.register()
    def test_function():
        pass

    assert test_function.slug == "test_function"

    @simple_registry.register()
    def TestClass():
        pass

    assert TestClass.slug == "TestClass"
