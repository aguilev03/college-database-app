import sqlite3


def write_to_database(file, instructions, values=None):
    """
    Executes a write operation on the specified SQLite database.

    This function connects to the SQLite database specified by the 'file' parameter,
    executes the SQL command provided in the 'instructions' parameter with the
    provided values, commits the changes, and then closes the connection.

    Parameters:
    file (str): The path to the SQLite database file.
    instructions (str): The SQL command to execute (e.g., INSERT, UPDATE, DELETE).
    values (tuple, optional): A tuple containing the values to safely substitute into the SQL command.

    Returns:
    None
    """
    conn = sqlite3.connect(file)
    c = conn.cursor()
    if values:
        c.execute(instructions, values)
    else:
        c.execute(instructions)
    conn.commit()
    conn.close()


def read_from_database(file, instructions, action="all", values=None):
    """
    Executes a read operation on the specified SQLite database and retrieves the results.

    This function connects to the SQLite database specified by the 'file' parameter,
    executes the SQL query provided in the 'instructions' parameter, and retrieves
    the data based on the specified 'action'. The connection to the database is closed
    after the operation.

    Parameters:
    file (str): The path to the SQLite database file.
    instructions (str): The SQL query to execute (e.g., SELECT).
    action (str or tuple): Determines the amount of data to fetch from the query.
        - "all": Fetches all rows from the result set.
        - "one": Fetches a single row from the result set.
        - ("many", int): Fetches a specified number of rows (int) from the result set.

    Returns:
    list or tuple or None:
        - If action is "all", returns a list of tuples containing all rows.
        - If action is "one", returns a single tuple representing one row or None if no more rows are available.
        - If action is ("many", int), returns a list of tuples containing the specified number of rows.
    """
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        if values:
            c.execute(instructions, values)
        else:
            c.execute(instructions)

        if action == "one":
            data = c.fetchone()
        elif isinstance(action, tuple) and action[0] == "many":
            data = c.fetchmany(action[1])
        else:  # Default action is "all"
            data = c.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        data = None
    finally:
        c.close()
        conn.close()
    return data


def initial_write(file):
    """
    Initializes the database with required tables and populates them with dummy data.

    This function creates the following tables in the specified SQLite database:
    - departments
    - courses
    - students
    - instructors
    - staff
    - course_students (junction table for courses and students)
    - course_instructors (junction table for courses and instructors)

    It also inserts initial dummy data into each table, providing sample departments,
    courses, students, instructors, and staff records.

    Parameters:
    file (str): The path to the SQLite database file where the tables and data will be created.

    Returns:
    None
    """
    create_departments_sql = """CREATE TABLE departments (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                description TEXT               
                                )"""

    department_dummy_data_sql = """INSERT INTO departments (name, description) VALUES
                                    ('Computer Science', 'Department of Computer Science and Engineering'),
                                    ('Mathematics', 'Department of Mathematics and Statistics'),
                                    ('Physics', 'Department of Physics'),
                                    ('English', 'Department of English Language and Literature');"""

    create_courses_sql = """CREATE TABLE courses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            department_id INTEGER,
                            description TEXT,
                            credits INTEGER,
                            FOREIGN KEY (department_id) REFERENCES departments(id)
                            );"""

    courses_dummy_data_sql = """INSERT INTO courses (name, department_id, description, credits) VALUES
                                ('Introduction to Computer Science', 1, 'An introductory course in computer science', 3),
                                ('Data Structures', 1, 'Study of data structures such as arrays, linked lists, etc.', 4),
                                ('Calculus I', 2, 'An introductory course in calculus', 4),
                                ('Physics I', 3, 'Basic principles of physics with laboratory', 4),
                                ('English Literature', 4, 'Survey of English literature', 3);"""

    create_students_sql = """CREATE TABLE students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            major TEXT
                            );"""

    students_dummy_data_sql = """INSERT INTO students (name, email, major) VALUES
                                ('Alice Johnson', 'alice.johnson@example.com', 'Computer Science'),
                                ('Bob Smith', 'bob.smith@example.com', 'Mathematics'),
                                ('Carol Davis', 'carol.davis@example.com', 'Physics'),
                                ('David Brown', 'david.brown@example.com', 'English'),
                                ('Eva Green', 'eva.green@example.com', 'Computer Science');
                                """

    create_instructors_table = """CREATE TABLE instructors (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                department_id INTEGER,
                                FOREIGN KEY (department_id) REFERENCES departments(id)
                                );"""
    instructors_dummy_data = """INSERT INTO instructors (name, email, department_id) VALUES
                                ('Dr. Jane Doe', 'jane.doe@example.com', 1),
                                ('Prof. John Smith', 'john.smith@example.com', 2),
                                ('Dr. Alice White', 'alice.white@example.com', 3),
                                ('Prof. Michael Brown', 'michael.brown@example.com', 4),
                                ('Dr. Emily Green', 'emily.green@example.com', 1);
                                """

    create_staff_table = """CREATE TABLE staff (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            role TEXT NOT NULL,
                            department_id INTEGER,
                            FOREIGN KEY (department_id) REFERENCES departments(id)
                            );"""
    staff_dummy_data = """INSERT INTO staff (name, role, department_id) VALUES
                        ('Susan Lee', 'Administrative Assistant', 1),
                        ('Mark Thompson', 'Lab Technician', 3),
                        ('Anna Kim', 'Student Counselor', 2),
                        ('Paul Roberts', 'Facilities Manager', NULL),
                        ('Laura Davis', 'Library Assistant', 4);
                        """
    create_junction_course_students_table = """CREATE TABLE course_students (
                                            course_id INTEGER,
                                            student_id INTEGER,
                                            PRIMARY KEY (course_id, student_id),
                                            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                                            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                                            );"""
    course_student_dummy_data = """INSERT INTO course_students (course_id, student_id) VALUES
                                (1, 1),
                                (1, 2),
                                (2, 1),
                                (2, 3),
                                (3, 4);
                                """

    create_junction_course_instructors_table = """CREATE TABLE course_instructors (
                                                course_id INTEGER,
                                                instructor_id INTEGER,
                                                PRIMARY KEY (course_id, instructor_id),
                                                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                                                FOREIGN KEY (instructor_id) REFERENCES instructors(id) ON DELETE CASCADE
                                                );"""

    course_instructors_dummy_data = """INSERT INTO course_instructors (course_id, instructor_id) VALUES
                                    (1, 1),
                                    (2, 1),
                                    (3, 2),
                                    (4, 3),
                                    (5, 4);
                                    """

    bulk_create_tables = [
        create_departments_sql,
        create_courses_sql,
        create_students_sql,
        create_instructors_table,
        create_staff_table,
        create_junction_course_students_table,
        create_junction_course_instructors_table,
    ]

    bulk_dummy_data = [
        department_dummy_data_sql,
        courses_dummy_data_sql,
        students_dummy_data_sql,
        instructors_dummy_data,
        staff_dummy_data,
        course_student_dummy_data,
        course_instructors_dummy_data,
    ]

    for table in bulk_create_tables:
        write_to_database(file, table)

    for dummy_data in bulk_dummy_data:
        write_to_database(file, dummy_data)


def main():
    """
    Main function to test database operations.

    This function initializes a SQLite database file named 'college_data.db'.
    It then reads all records from the 'students' table and prints them.

    The function demonstrates the use of the `read_from_database` function to
    query data from the database.

    Parameters:
    None

    Returns:
    None
    """

    database_file = "college_data.db"

    test = read_from_database(database_file, "SELECT * FROM students")
    print(test)


if __name__ == "__main__":
    main()
