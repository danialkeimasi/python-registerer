import pytest

from registerer import Registerer


@pytest.fixture
def simple_registry():
    return Registerer(slug_attr="slug")


@pytest.fixture
def function():
    return lambda: None


@pytest.fixture
def Parent():
    return type("Parent", (), {})


@pytest.fixture
def Child(Parent):
    return type("Child", (Parent,), {})


@pytest.fixture
def parent_registry(Parent):
    return Registerer(parent_class=Parent)
