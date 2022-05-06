from fast_registry import FastRegistry, RegistrationError, RegistryValidator


class Animal:
    is_wild: bool = None


class OnlyDomestic(RegistryValidator):
    def on_register(self, slug, item, registry_dict):
        if item.is_wild:
            raise RegistrationError(
                f"{item.__name__} is wild, only domestic animals are allowed to register."
            )


domestic_animals_registry = FastRegistry(Animal, validators=[OnlyDomestic()])

# success:
@domestic_animals_registry.register("cow")
class Cow(Animal):
    is_wild = False


# failure:
# raises fast_registry.exceptions.RegistrationError: Lion is wild, only domestic animals are allowed to register.
@domestic_animals_registry.register("lion")
class Lion(Animal):
    is_wild = True
