from fast_registry import FastRegistry, FunctionAnnotationValidator, RegistrationError

database_registry = FastRegistry(
    validators=[
        FunctionAnnotationValidator(annotations=[("name", str)]),
    ]
)

# success:
@database_registry.register("sqlite")
def sqlite_database_connection(name: str):
    return f"sqlite connection {name}"


# failure:
# fast_registry.exceptions.RegistrationError: The 'postgres_database_connection' function with slug='postgres' do not match the expected annotations.
# Expected: [('name', <class 'str'>)]
# Got: [('name', <class 'str'>), ('host', <class 'str'>)]
@database_registry.register("postgres")
def postgres_database_connection(name: str, host: str):
    return f"postgres connection {name}"


def main():
    print(database_registry.get("postgres")("personal"))  # postgres connection personal


if __name__ == "__main__":
    main()
