import sqlite3


def write_to_database(file, instructions):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute(instructions)
    conn.commit()
    conn.close()


def main():
    database_file = "college_data.db"

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

    write_to_database(database_file, create_departments_sql)
    write_to_database(database_file, department_dummy_data_sql)


if __name__ == "__main__":
    main()
