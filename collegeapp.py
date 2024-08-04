import database_functions


class Tables:
    def __init__(self) -> None:
        pass

    def create_row(self, table_name, values, file):
        command = f"INSERT INTO {table_name} VALUES ({values})"
        database_functions.write_to_database(file, command)


class Departments:
    def __init__(self, name, description):
        self.name = name
        self.description = description
