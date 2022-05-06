from fast_registry import FastRegistry


class Animal:
    def talk(self):
        raise NotImplementedError


# create a registry that requires registered items to implement the Animal interface:
animal_registry = FastRegistry(Animal)


@animal_registry.register("dog")
class Dog(Animal):
    def talk(self):
        return "woof"


def main():
    print(animal_registry.get("dog"))  # <class '__main__.Dog'>
    print(animal_registry.get("dog")())  # <__main__.Dog object at 0x7f108ad37d60>
    print(animal_registry.get("dog")().talk())  # woof


if __name__ == "__main__":
    main()
