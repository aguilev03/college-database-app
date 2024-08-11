import database_functions


class Tables:
    def __init__(self):
        self.file = "college_data.db"

    def validation(self, table, columns, value, comparison, extra=None):
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
        if extra is None:
            command = f"SELECT {columns} FROM {table} WHERE {value} = ?"
            result = database_functions.read_from_database(
                self.file, command, "one", (comparison,)
            )
            if result:
                return True
            else:
                return False
        else:
            command = f"""SELECT {columns} FROM {table}
                        WHERE {value[0]} = ? AND {value[1]} = ?"""
            result = database_functions.read_from_database(
                self.file, command, "one", comparison
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
        command = f"""INSERT INTO {table_name} 
                    VALUES ({placeholders})"""

        return database_functions.write_to_database(self.file, command, values)

    def update_row(self, table_name, primary, primary_value, changes):
        """
        Updates a row in the specified table based on the primary key.

        This function constructs an SQL UPDATE statement to modify a row in the specified
        table. It updates the columns as specified in the `changes` parameter where the
        primary key column matches the provided value.

        Parameters:
        table_name (str): The name of the table where the row needs to be updated.
        primary (str): The primary key column used to identify the row.
        primary_value (str or int): The value of the primary key to match the row.
        changes (dict): A dictionary specifying the columns and their new values.

        Returns:
        None
        """
        placeholders = ", ".join([f"{key} = ?" for key in changes.keys()])
        command = f"""UPDATE {table_name}
                SET {placeholders}
                WHERE {primary} = ?"""
        values = tuple(changes.values()) + (primary_value,)
        return database_functions.write_to_database(self.file, command, values)

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

            return database_functions.write_to_database(
                self.file, command, (primary_value,)
            )
        else:
            command = f"""DELETE FROM {table_name} WHERE {primary_key[0]} = ? AND {primary_key[1]} = ?"""

            return database_functions.write_to_database(
                self.file, command, (primary_value[0], primary_value[1])
            )

    def get_id(self, table, query):
        """
        Retrieves the ID of a row from the specified table where the name matches the query.

        This function constructs an SQL SELECT statement to fetch the ID of a row
        from the given table where the 'name' column matches the specified query value.
        It uses a parameterized query to ensure safe execution and prevent SQL injection.

        Parameters:
        table (str): The name of the table to search in.
        query (str): The value to match in the 'name' column.

        Returns:
        int or None: The ID of the matching row if found, otherwise None.
        """
        command = f"SELECT id FROM {table} WHERE name = ?"
        result = database_functions.read_from_database(
            self.file, command, (query,), "one"
        )
        if id:
            return id[0]
        else:
            return None


class Departments(Tables):
    def __init__(self, name, description, id=None):
        self.name = name
        self.description = description
        self.table = "departments"
        self.file = "college_data.db"
        self.id = id

    def add(self):
        if self.id is None:
            table = f"{self.table} (name, description)"
            return self.create_row(table, (self.name, self.description))

    def remove(self):
        if self.id is not None:
            self.delete_row(self.table, "id", self.id)

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
        changes = {}
        if name is not None:
            changes["name"] = name
        if description is not None:
            changes["description"] = description

        if changes:
            if id is None:
                return "Department doesn't exist"
            else:
                return self.update_row(self.table, "id", self.id, changes)

    def refresh(self):
        command = "SELECT * FROM departments WHERE id = ?"
        query_result = database_functions.read_from_database(
            self.file, command, "one", (self.id,)
        )

        self.name = query_result[1]
        self.description = query_result[2]


class Courses(Tables):
    def __init__(self, name, department_id, description, credits, id=None):
        self.name = name
        self.department_id = department_id
        self.description = description
        self.credits = credits
        self.file = "college_data.db"
        self.table = "courses"
        self.id = id

    def add(self):
        table = f"{self.table} (name, department_id, description, credits)"
        if self.id is None:
            active_department = self.validation(
                "departments", "*", "id", self.department_id
            )
            if active_department:
                return self.create_row(
                    table,
                    (self.name, self.department_id, self.description, self.credits),
                )
            else:
                return "Invalid Department"

    def remove(self):
        if self.id is not None:
            self.delete_row("course_students", "course_id", self.id)
            self.delete_row("course_instructors", "course_id", self.id)
            self.delete_row(self.table, "id", self.id)

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
        changes = {}
        if name is not None:
            changes["name"] = name
        if department_id is not None:
            changes["department_id"] = department_id
        if description is not None:
            changes["description"] = description
        if credits is not None:
            changes["credits"] = credits

        if changes:
            if id is None:
                return "Course doesn't exist"
            else:
                active_department = self.validation(
                    "departments", "*", "id", self.department_id
                )
            if active_department:
                return self.update_row(self.table, "id", self.id, changes)

    def get_department_name(self):
        command = """SELECT 
                        name AS department_name
                    FROM 
                        departments
                    WHERE 
                        id = ?;
                    """
        return database_functions.read_from_database(
            self.file,
            command,
            "one",
            (self.department_id,),
        )

    def refresh(self):
        command = "SELECT * FROM courses WHERE id = ?"
        query_result = database_functions.read_from_database(
            self.file, command, "one", (self.id,)
        )

        self.name = query_result[1]
        self.department_id = query_result[2]
        self.description = query_result[3]
        self.credits = query_result[4]


class Students(Tables):
    def __init__(self, name, email, major, id=None):
        self.name = name
        self.email = email
        self.major = major
        self.file = "college_data.db"
        self.table = "students"
        self.id = id

    def add(self):
        if self.id is None:
            table = f"{self.table} (name, email, major)"
            self.create_row(table, (self.name, self.email, self.major))
            print("Student added")

    def update(self, name=None, email=None, major=None, id=None):
        """
        Updates the department's name or description.

        Parameters:
        name (str): The new name for the department (optional).
        description (str): The new description for the department (optional).

        Note:
        Only the provided attributes will be updated. If both are provided,
        both will be updated.
        """
        changes = {}
        if name is not None:
            changes["name"] = name
        if email is not None:
            changes["email"] = email
        if major is not None:
            changes["major"] = major

        if changes:
            if id is None:
                return "Error"
            else:
                self.update_row(self.table, "id", self.id, changes)
                return "successfully updated"

    def enroll(self, course_id):
        if self.id is not None:
            class_exist = self.validation("courses", "*", "id", course_id)

            if class_exist:
                enrolled_check = self.validation(
                    "course_students", "*", course_id, self.id
                )
                print(enrolled_check)
                if enrolled_check == False:
                    self.create_row(
                        "course_students (course_id, student_id)", (course_id, self.id)
                    )

    def withdrawl(self, course_id):

        enrolled_check = self.validation(
            "course_students",
            "*",
            ("course_id", "student_id"),
            (course_id, self.id),
            "a",
        )
        print(enrolled_check)
        if enrolled_check:
            self.delete_row(
                "course_students",
                ("course_id", "student_id"),
                (course_id, self.id),
                "A",
            )

    def remove(self):
        if self.id is not None:
            self.delete_row(self.table, "id", self.id)

    def get_courses(self):

        command = """SELECT 
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.description AS course_description,
                        courses.credits AS course_credits,
                        instructors.id AS instructor_id,
                        instructors.name AS instructor_name,
                        instructors.email AS instructor_email
                    FROM 
                        courses
                    JOIN 
                        course_students ON courses.id = course_students.course_id
                    JOIN 
                        students ON course_students.student_id = students.id
                    JOIN 
                        course_instructors ON courses.id = course_instructors.course_id
                    JOIN 
                        instructors ON course_instructors.instructor_id = instructors.id
                    WHERE 
                        students.id = ?"""
        query_result = database_functions.read_from_database(
            self.file, command, "all", (self.id,)
        )

        columns = [
            "course_id",
            "course_name",
            "course_description",
            "course_credits",
            "instructor_id",
            "instructor_name",
            "instructor_email",
        ]
        student_courses = [dict(zip(columns, row)) for row in query_result]
        return student_courses

    def refresh(self):
        command = "SELECT * FROM students WHERE id = ?"
        query_result = database_functions.read_from_database(
            self.file, command, "one", (self.id,)
        )
        print(query_result)

        self.name = query_result[1]
        self.email = query_result[2]
        self.major = query_result[3]


class Instructors(Tables):
    def __init__(self, name, email, department_id, id=None):
        self.name = name
        self.email = email
        self.file = "college_data.db"
        self.department_id = department_id
        self.table = "instructors"
        self.id = id

    def add(self):
        table = f"{self.table} (name, email, department_id)"
        if self.id is None:
            active_department = self.validation(
                "departments", "*", "id", self.department_id
            )
            if active_department:
                return self.create_row(
                    table, (self.name, self.email, self.department_id)
                )

            else:
                return "Department doesn't exist"

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
        changes = {}
        if name is not None:
            changes["name"] = name
        if email is not None:
            changes["email"] = email
        if department_id is not None:
            changes["department_id"] = department_id

        if changes:
            if id is None:
                return "Instructor doesn't exist"
            else:
                active_department = self.validation(
                    "departments", "*", "id", self.department_id
                )
            if active_department:
                return self.update_row(self.table, "id", self.id, changes)

    def assign_course(self, course_id):
        if self.id is not None:
            class_exist = self.validation("courses", "*", "id", course_id)
            if class_exist:
                assigned_check = self.validation(
                    "course_instructors",
                    "*",
                    ("course_id", "instructor_id"),
                    (course_id, self.id),
                    "a",
                )
                if assigned_check == False:
                    self.create_row(
                        "course_instructors (course_id, instructor_id)",
                        (course_id, self.id),
                    )

    def unassign(self, course_id):
        assigned_check = self.validation(
            "course_instructors",
            "*",
            ("course_id", "instructor_id"),
            (course_id, self.id),
            "a",
        )
        if assigned_check:
            self.delete_row(
                "course_instructors",
                ("course_id", "instructor_id"),
                (course_id, self.id),
                "A",
            )

    def remove(self):
        if self.id is not None:
            self.delete_row(self.table, "id", self.id)

    def get_courses(self):

        command = """SELECT 
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.description AS course_description,
                        courses.credits AS course_credits
                    FROM 
                        courses
                    JOIN 
                        course_instructors ON courses.id = course_instructors.course_id
                    JOIN 
                        instructors ON course_instructors.instructor_id = instructors.id
                    WHERE 
                        instructors.id = ?;"""
        query_result = database_functions.read_from_database(
            self.file, command, "all", (self.id,)
        )

        columns = [
            "course_id",
            "course_name",
            "course_description",
            "course_credits",
        ]
        instructor_courses = [dict(zip(columns, row)) for row in query_result]
        return instructor_courses

    def get_department_name(self):
        command = """SELECT 
                        name AS department_name
                    FROM 
                        departments
                    WHERE 
                        id = ?;
                    """
        return database_functions.read_from_database(
            self.file,
            command,
            "one",
            (self.department_id,),
        )

    def get_assigned_courses(self):
        command = """SELECT 
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.description AS course_description,
                        courses.credits AS course_credits
                    FROM 
                        courses
                    JOIN 
                        course_instructors ON courses.id = course_instructors.course_id
                    JOIN 
                        instructors ON course_instructors.instructor_id = instructors.id
                    WHERE 
                        instructors.id = ?;"""

        query_result = database_functions.read_from_database(
            self.file, command, "all", (self.id,)
        )
        columns = ["course_id", "course_name", "course_description", "course_credits"]
        assigned_courses = [dict(zip(columns, row)) for row in query_result]
        return assigned_courses

    def refresh(self):
        command = "SELECT * FROM instructors WHERE id = ?"
        query_result = database_functions.read_from_database(
            self.file, command, "one", (self.id,)
        )
        print(query_result)

        self.name = query_result[1]
        self.email = query_result[2]
        self.department_id = query_result[3]


class Staff(Tables):
    def __init__(self, name, role, id=None):
        self.name = name
        self.role = role
        self.file = "college_data.db"
        self.table = "staff"
        self.id = id

    def add(self):

        if self.id is None:
            table = f"{self.table} (name, role, department_id)"
            return self.create_row(table, (self.name, self.role, "NULL"))

    def remove(self):
        if self.id is not None:
            return self.delete_row(self.table, "id", self.id)

    def update_staff(self, name=None, role=None, id=None):
        """
        Updates the department's name or description.

        Parameters:
        name (str): The new name for the department (optional).
        description (str): The new description for the department (optional).

        Note:
        Only the provided attributes will be updated. If both are provided,
        both will be updated.
        """
        changes = {}
        if name is not None:
            changes["name"] = name
        if role is not None:
            changes["role"] = role
        if id is None:
            self.id = self.get_id(self.table, "id")

        if changes:
            return self.update_row(self.table, "id", self.id, changes)

    def refresh(self):
        command = "SELECT * FROM staff WHERE id = ?"
        query_result = database_functions.read_from_database(
            self.file, command, "one", (self.id,)
        )

        self.name = query_result[1]
        self.role = query_result[2]


class Student_views:
    def __init__(self):
        self.file = "college_data.db"

    def get_students(self):

        command = "SELECT * FROM students"
        query_result = database_functions.read_from_database(self.file, command)
        columns = ["id", "name", "email", "major"]
        students_list = [dict(zip(columns, row)) for row in query_result]
        return students_list

    def get_student_classes(self, id):
        command = """SELECT 
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.description AS course_description,
                        courses.credits AS course_credits,
                        instructors.id AS instructor_id,
                        instructors.name AS instructor_name,
                        instructors.email AS instructor_email
                    FROM 
                        courses
                    JOIN 
                        course_students ON courses.id = course_students.course_id
                    JOIN 
                        students ON course_students.student_id = students.id
                    JOIN 
                        course_instructors ON courses.id = course_instructors.course_id
                    JOIN 
                        instructors ON course_instructors.instructor_id = instructors.id
                    WHERE 
                        students.id = ?"""
        query_result = database_functions.read_from_database(
            self.file, command, "all", (id,)
        )
        columns = [
            "course_id",
            "course_name",
            "course_description",
            "course_credits",
            "instructor_id",
            "instructor_name",
            "instructor_email",
        ]
        student_courses = [dict(zip(columns, row)) for row in query_result]
        return student_courses

    def get_all_courses(self):
        command = """SELECT
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.description AS course_description,
                        courses.credits AS course_credits,
                        instructors.id AS instructor_id,
                        instructors.name AS instructor_name,
                        instructors.email AS instructor_email
                    FROM
                        courses
                    JOIN
                        course_instructors ON courses.id = course_instructors.course_id
                    JOIN 
                        instructors ON course_instructors.instructor_id = instructors.id"""
        query_result = database_functions.read_from_database(self.file, command)

        columns = [
            "course_id",
            "course_name",
            "course_description",
            "course_credits",
            "instructors_id",
            "instructor_name",
            "instructor_email",
        ]
        all_courses = [dict(zip(columns, row)) for row in query_result]
        return all_courses

    def get_all_instructors(self):

        command = """SELECT 
    instructors.id AS instructor_id,
    instructors.name AS instructor_name,
    instructors.email AS instructor_email,
    departments.id AS department_id,
    departments.name AS department_name,
    departments.description AS department_description
FROM 
    instructors
JOIN 
    departments 
ON 
    instructors.department_id = departments.id;

                    """
        query_result = database_functions.read_from_database(self.file, command)
        columns = [
            "id",
            "name",
            "email",
            "department_id",
            "department_name",
            "department_descriptions",
        ]
        instructor_list = [dict(zip(columns, row)) for row in query_result]
        return instructor_list

    def get_all_departments(self):
        command = "SELECT * FROM departments"
        query_result = database_functions.read_from_database(self.file, command)
        columns = ["id", "name", "description"]
        course_list = [dict(zip(columns, row)) for row in query_result]
        return course_list

    def get_courses_info(self):
        command = """SELECT 
                        courses.id AS course_id,
                        courses.name AS course_name,
                        courses.credits AS course_credits,
                        courses.description AS course_description,
                        COUNT(DISTINCT course_students.student_id) AS student_count,
                        COUNT(DISTINCT course_instructors.instructor_id) AS instructor_count
                    FROM 
                        courses
                    LEFT JOIN 
                        course_students ON courses.id = course_students.course_id
                    LEFT JOIN 
                        course_instructors ON courses.id = course_instructors.course_id
                    GROUP BY 
                        courses.id, courses.name;
                    """
        query_result = database_functions.read_from_database(self.file, command)
        columns = [
            "course_id",
            "course_name",
            "course_credits",
            "course_description",
            "student_count",
            "instructor_count",
        ]
        course_list = [dict(zip(columns, row)) for row in query_result]
        return course_list

    def get_all_courses(self):
        command = "SELECT * FROM courses"
        query_result = database_functions.read_from_database(self.file, command)
        columns = ["id", "name", "department_id", "description", "credits"]
        course_list = [dict(zip(columns, row)) for row in query_result]
        return course_list

    def get_all_staff(self):
        command = "SELECT * FROM staff"
        query_result = database_functions.read_from_database(self.file, command)
        columns = ["id", "name", "role", "department_id"]
        staff_list = [dict(zip(columns, row)) for row in query_result]
        return staff_list
