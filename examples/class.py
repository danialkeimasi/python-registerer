from registerer import Registerer


class Animal:
    def talk(self) -> None:
        raise NotImplementedError


# create a registry that requires registered items to implement the Animal interface:
animal_registry = Registerer(Animal)


@animal_registry.register("dog")
class Dog(Animal):
    def talk(self) -> None:
        return "woof"


def main():
    print(animal_registry["dog"])  # <class '__main__.Dog'>
    print(animal_registry["dog"]())  # <__main__.Dog object at 0x7f108ad37d60>
    print(animal_registry["dog"]().talk())  # woof


if __name__ == "__main__":
    main()
