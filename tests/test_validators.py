import pytest

from registerer import Registerer, RegistrationError, RegistryValidator


def test_validator(Parent, Child):
    registry = Registerer(
        slug_attr="slug",
        validators=[
            RegistryValidator(
                lambda item: item.slug != "no",
                error="oh no, registered class is not ok!",
            ),
        ],
    )

    registry.register("Foo")(Parent)

    with pytest.raises(RegistrationError):
        registry.register("no")(Child)
