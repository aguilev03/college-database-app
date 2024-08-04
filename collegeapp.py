import database_functions


class Tables:
    def __init__(self):
        self.file = "college_data.db"

    def validation(
        self,
        table,
        columns,
        value,
        comparison,
    ):
        """
        Validates the existence of a record in a specified table based on a condition.

        This function checks if there exists at least one record in the specified
        SQL table that meets the given condition. It queries the table for a specific
        value in a specified column and returns True if the value is found, otherwise False.

        Parameters:
        table (str): The name of the table to query.
        columns (str): The column(s) to select from the table.
        value (str): The column name to compare against.
        comparison (str or int): The value to search for in the specified column.
        file (str): The path to the SQLite database file.

        Returns:
        bool: True if the record exists, False otherwise.
        """
        command = f"SELECT {columns} FROM {table} WHERE {value} = ?"
        result = database_functions.read_from_database(
            self.file, (command, (comparison)), "one"
        )
        if result:
            return True
        else:
            return False

    def create_row(self, table_name, values):
        """
        Inserts a new row into the specified table in the database.

        This method constructs an SQL INSERT statement to add a new row into the
        specified table with the provided values. The values are safely inserted
        into the database using parameterized queries to prevent SQL injection.

        Parameters:
        table_name (str): The name of the table to insert the new row into.
        values (tuple): A tuple containing the values to insert into the table.
                        The order of values should match the table's column order.

        Returns:
        None
        """
        placeholders = ", ".join(["?"] * len(values))
        command = f"INSERT INTO {table_name} VALUES ({placeholders})"
        database_functions.write_to_database(self.file, command, values)

    def update_row(self, table_name, primary, primary_value, changes):
        command = f"""UPDATE {table_name}
                SET {changes} 
                WHERE {primary} = '{primary_value} """
        database_functions.write_to_database(self.file, command)

    def delete_row(self, table_name, primary_key, primary_value, extra_arguments=None):
        """
        Deletes a row from the specified table in the database based on the primary key value.

        This function constructs an SQL DELETE statement to remove a row from the given
        table where the primary key column matches the provided value. The function uses
        parameterized queries to ensure the operation is safe and prevent SQL injection.

        Parameters:
        table_name (str): The name of the table from which to delete the row.
        primary (str): The name of the primary key column used to identify the row.
        primary_value (str or int): The value of the primary key for the row to delete.

        Returns:
        None
        """
        if extra_arguments is None:
            command = f"DELETE FROM {table_name} WHERE {primary_key} = ?"
            database_functions.write_to_database(self.file, command, (primary_value,))
        else:
            command = f"DELETE FROM {table_name} WHERE {primary_key[0]} = ? AND {primary_value[1]} = ?"
            database_functions.write_to_database(self.file, command, primary_value)

    def get_id(self, table, query):
        command = f"SELECT id FROM ? WHERE name = ?"
        id = database_functions.read_from_database(self.file, command, "one")
        if id:
            return id[0]
        else:
            return None


class Departments(Tables):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.id = None

    def update_department(self, name=None, description=None, id=None):
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
        if id is not None:
            self.id = id


class Courses(Tables):
    def __init__(self, name, department_id, description, credits):
        self.name = name
        self.department_id = department_id
        self.description = description
        self.credits = credits
        self.id = None

    def update_course(
        self, name=None, department_id=None, description=None, credits=None, id=None
    ):
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
        if department_id is not None:
            self.department_id = department_id
        if description is not None:
            self.description = description
        if credits is not None:
            self.credits = credits
        if id is not None:
            self.id = id


class Students(Tables):
    def __init__(self, name, email, major):
        self.name = name
        self.email = email
        self.major = major
        self.id = None

    def update_student(self, name=None, email=None, major=None, id=None):
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
        if email is not None:
            self.email = email
        if major is not None:
            self.major = major
        if id is not None:
            self.id = id

    def enroll(self, course_id):
        if self.id is not None:
            class_exist = self.validation("courses", "*", "id", course_id)
            if class_exist:
                enrolled_check = self.validation(
                    "course_students", "*", course_id, self.id
                )
                if enrolled_check == False:
                    self.create_row("course_students", (course_id, self.id))

    def withdrawl(self, course_id):
        enrolled_check = self.validation("course_students", "*", course_id, self.id)
        if enrolled_check:
            self.delete_row(
                "course_students", ("course_id", "student_id"), (course_id, self.id)
            )


class Instructors(Tables):
    def __init__(self, name, email, department_id):
        self.name = name
        self.email = email
        self.department_id = department_id
        self.id = None

    def update_instructor(self, name=None, email=None, department_id=None, id=None):
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
        if email is not None:
            self.email = email
        if department_id is not None:
            self.department_id = department_id
        if id is not None:
            self.id = id

    def assign_course(self, course_id):
        if self.id is not None:
            class_exist = self.validation("courses", "*", "id", course_id)
            if class_exist:
                assigned_check = self.validation(
                    "course_instructors", "*", course_id, self.id
                )
                if assigned_check == False:
                    self.create_row("course_instructors", (course_id, self.id))

    def unassign(self, course_id):
        assigned_check = self.validation("course_instructors", "*", course_id, self.id)
        if assigned_check:
            self.delete_row(
                "course_instructors",
                ("course_id", "instructor_id"),
                (course_id, self.id),
            )


class Staff(Tables):
    def __init__(self, name, role, department_id):
        self.name = name
        self.role = role
        self.department_id = department_id
        self.id = None

    def update_staff(self, name=None, role=None, department_id=None, id=None):
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
        if role is not None:
            self.role = role
        if department_id is not None:
            self.department_id = department_id
        if id is not None:
            self.id = id
