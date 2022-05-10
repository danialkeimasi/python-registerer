from registerer import Registerer

database_registry = Registerer()


@database_registry.register("sqlite")
def sqlite_database_connection():
    return "sqlite connection"


@database_registry.register("postgres")
def postgres_database_connection():
    return "postgres connection"


def main():
    print(database_registry.get("postgres")())  # postgres connection


if __name__ == "__main__":
    main()
