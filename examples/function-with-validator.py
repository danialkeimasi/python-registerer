import registerer

database_registry = registerer.Registerer(
    validators=[registerer.RegistryValidator(lambda item: not getattr(item, "fail", False))]
)

# success:
@database_registry.register("sqlite")
def sqlite_database_connection(name: str):
    return f"sqlite connection {name}"


# failure:
# registerer.exceptions.RegistrationError: custom validation failed when registering postgres_database_connection
@database_registry.register("postgres", fail=True)
def postgres_database_connection(name: str):
    return f"postgres connection {name}"


def main():
    print(database_registry["postgres"]("personal"))  # postgres connection personal


if __name__ == "__main__":
    main()
