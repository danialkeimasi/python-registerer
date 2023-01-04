import pytest

from registerer import Registerer, RegistrationError, RegistryValidator


def test_validator():

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

    with pytest.raises(RegistrationError):

        @registry.register("no")
        class Foo2:
            pass
