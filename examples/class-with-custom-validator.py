import registerer


class Animal:
    is_wild: bool = None


domestic_animals_registry = registerer.Registerer(
    Animal,
    max_size=4,
    validators=[
        registerer.RegistryValidator(
            lambda item: not item.is_wild,
            error="only domestic animals allowed.",  # Optional
        ),
    ],
)


# success:
@domestic_animals_registry.register("cow")
class Cow(Animal):
    is_wild = False


# failure:
# raises registerer.exceptions.RegistrationError: Lion is wild, only domestic animals are allowed to register.
@domestic_animals_registry.register("lion")
class Lion(Animal):
    is_wild = True
