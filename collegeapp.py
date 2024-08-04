import database_functions


class Tables:
    def __init__(self):
        self.file = "college_data.db"

    def create_row(self, table_name, values):
        command = f"INSERT INTO {table_name} VALUES ({values})"
        database_functions.write_to_database(self.file, command)

    def update_row(self, table_name, primary, primary_value, changes):
        command = f"""UPDATE {table_name}
                SET {changes} 
                WHERE {primary} = '{primary_value} """
        database_functions.write_to_database(self.file, command)

    def delete_row(self, table_name, primary, primary_value):
        command = "DELETE FROM ? WHERE ? = ?,", (table_name, primary, primary_value)
        database_functions.write_to_database(self.file, command)

    def get_id(self, table, query):
        command = f"SELECT id FROM ? WHERE name = ?"
        id = database_functions.read_from_database(self.file, command, 1)


class Departments:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def update_department(self, name=None, description=None):
        """
        Updates the department's name or description.

        Parameters:
        name (str): The new name for the department (optional).
        description (str): The new description for the department (optional).

        Note:
        Only the provided attributes will be updated. If both are provided,
        both will be updated.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
