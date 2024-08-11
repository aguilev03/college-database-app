# College Database Management System

This project is a simple database management system for a college. The system manages various entities within the college, such as departments, courses, students, instructors, and staff. It allows users to perform CRUD (Create, Read, Update, Delete) operations on these entities through a terminal-based interface.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Classes and Functions](#classes-and-functions)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features
- **Departments Management**: Add, view, update, and remove departments.
- **Courses Management**: Add, view, update, and remove courses within departments.
- **Students Management**: Enroll students in courses, update student details, and manage their enrollments.
- **Instructors Management**: Assign instructors to courses, update instructor details, and manage their assignments.
- **Staff Management**: Track and manage other staff members working within the college.
- **Database Initialization**: Automatically creates and populates the database with initial data.
- **User-Friendly Interface**: Text-based interface for easy interaction.

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/college-database-management-system.git
    cd college-database-management-system
    ```

2. **Install Required Dependencies**:
    This project uses `sqlite3` and `curses` (for enhanced UI). Ensure you have Python 3.x installed. For Windows users:
    ```bash
    pip install windows-curses
    ```

3. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage
Once you start the application, you will be presented with a main menu allowing you to manage students, instructors, courses, staff, and departments. Use the arrow keys to navigate through the options and press `Enter` to select an option. You can exit the program by selecting the "Exit" option or pressing `q`.

### Main Menu Options:
- **Manage Students**: Enroll students in courses, update student details, or remove students.
- **Manage Instructors**: Assign instructors to courses, update instructor details, or remove instructors.
- **Manage Courses**: Add, view, update, or remove courses within departments.
- **Manage Staff**: Track and manage other staff members working within the college.
- **Manage Departments**: Add, view, update, or remove departments.
- **Admin: Database Reset**: Resets the database to its initial state, removing all existing data.

## File Structure
- `main.py`: The main entry point of the application. It contains the interface logic for managing different entities.
- `collegeapp.py`: Contains the core classes (`Departments`, `Courses`, `Students`, `Instructors`, `Staff`) and their associated methods.
- `README.md`: Documentation for the project.
- `college_data.db`: The SQLite database file used to store data (created automatically on first run).

## Classes and Functions
### `Departments`
- `add()`: Adds a new department to the database.
- `remove()`: Removes a department from the database.
- `update_department()`: Updates the department's details.
- `refresh()`: Refreshes the department's attributes from the database.

### `Courses`
- `add()`: Adds a new course to the database.
- `remove()`: Removes a course from the database.
- `update_course()`: Updates the course's details.
- `get_department_name()`: Retrieves the name of the department offering the course.
- `refresh()`: Refreshes the course's attributes from the database.

### `Students`
- `add()`: Adds a new student to the database.
- `update()`: Updates the student's details.
- `enroll()`: Enrolls the student in a course.
- `withdrawl()`: Withdraws the student from a course.
- `remove()`: Removes a student from the database.
- `get_courses()`: Retrieves the courses the student is enrolled in.
- `get_courses_info()`: Retrieves a summary of all courses.

### `Instructors`
- `add()`: Adds a new instructor to the database.
- `remove()`: Removes an instructor from the database.
- `update()`: Updates the instructor's details.
- `assign_course()`: Assigns the instructor to a course.
- `unassign_course()`: Unassigns the instructor from a course.
- `get_courses()`: Retrieves the courses the instructor is assigned to.

### `Staff`
- `add()`: Adds a new staff member to the database.
- `remove()`: Removes a staff member from the database.
- `update_staff()`: Updates the staff member's details.
- `refresh()`: Refreshes the staff member's attributes from the database.

### Utility Functions
- `write_to_database()`: Executes a write operation on the SQLite database.
- `read_from_database()`: Executes a read operation on the SQLite database and retrieves the results.
- `initial_write()`: Initializes the database with required tables and populates them with dummy data.

## Future Improvements
- **Enhanced User Interface**: Implement a more interactive interface using `curses` for better user experience.
- **Additional Features**: Expand functionality to include more detailed management of schedules, grades, and more advanced reporting.
- **Error Handling**: Implement more robust error handling and logging throughout the application.
- **Unit Testing**: Add unit tests to ensure code reliability and correctness.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
