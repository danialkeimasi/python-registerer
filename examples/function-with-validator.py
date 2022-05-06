from fast_registry import FastRegistry, FunctionAnnotationValidator

database_registry = FastRegistry(
    validators=[
        FunctionAnnotationValidator(annotations=[("name", str)]),
    ]
)


@database_registry.register("sqlite")
def sqlite_database_connection(name: str):
    return f"sqlite connection {name}"


@database_registry.register("postgres")
def postgres_database_connection(name: str):
    return f"postgres connection {name}"


def main():
    print(database_registry.get("postgres")("personal"))  # postgres connection personal


if __name__ == "__main__":
    main()
