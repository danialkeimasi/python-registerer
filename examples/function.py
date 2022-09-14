from registerer import Registerer

database_registry = Registerer()


@database_registry.register
def sqlite():
    return "sqlite connection"


@database_registry.register("postgres")
def postgres_backup():
    return "postgres connection"


def main():
    print(database_registry["sqlite"]())  # sqlite connection
    print(database_registry["postgres"]())  # postgres connection


if __name__ == "__main__":
    main()
