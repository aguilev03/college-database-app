import collegeapp
import os
import sys


def clear_screen():
    # Check if the system is Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Mac and Linux (os.name is 'posix')
    else:
        _ = os.system("clear")


def main_menu():
    menu = """
    Main Menu:
    1) Manage Students
    2) Manage Instructors
    3) Manage Courses
    4) Manage Staff
    5) Manage departments
    6) Exit\n
    9) ADMIN: DATABASE RESET
    """

    menu_options = {
        "1": manage_students,
        "2": manage_instructors,
        "3": manage_courses,
        "4": manage_staff,
        "5": manage_departments,
        "9": database_reset,
        "6": exit_program,
    }

    while True:
        clear_screen()
        print(menu)
        choice = input("Select an option: ").strip()

        if choice in menu_options:
            menu_options[choice]()
        else:
            print("Invalid choice, please try again.")


def manage_departments():
    while True:
        department_view = collegeapp.Student_views()
        department_list = {}
        department_list = department_view.get_all_departments()
        clear_screen()

        if department_list:
            for department in department_list:
                print(
                    f"ID: {department['id']}\t Department Name: {department['name']}\n",
                    f"Description: {department['description']}\n",
                )

        print("\nManage Departments Menu")
        print("1) Add Department")
        print("2) Remove Department")
        print("3) View Department")
        print("4) Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add Department logic here
            department_data = [
                input("Please enter Department Name: "),
                input("Please enter Department Description: "),
            ]

            clear_screen()

            new_department = collegeapp.Departments(
                department_data[0], department_data[1]
            )

            status = new_department.add()
            print(status)
            input()

        elif choice == "2":
            # Remove Department logic here
            department_id = input(
                "Please enter the Department ID you would like to remove: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                department_id = int(department_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            department_list = department_view.get_all_departments()
            department_found = False

            for department in department_list:
                if department["id"] == department_id:
                    department_found = True
                    department_delete = collegeapp.Departments(
                        department["name"], department["description"], department["id"]
                    )

                    clear_screen()
                    print(f"Department to delete: {department_delete.name}")

                    remove_choice = input(
                        "Remove this Department from the database? y/N "
                    ).strip()
                    if remove_choice.lower() == "y":
                        department_delete.remove()
                        print("Department removed successfully.")
                        input("Press Enter to continue...")
                    else:
                        print("Delete operation cancelled.")
                        input("Press Enter to continue...")
                    break  # Exit the loop once the student is found and action is taken

            if not department_found:
                print("Department with the given ID was not found.")
                input("Press Enter to continue...")

        elif choice == "3":
            # List Department logic here
            department_id = input(
                "Please enter the Department ID you would like to view: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                department_id = int(department_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            department_list = department_view.get_all_departments()
            department_found = False
            department_inspect = None
            for department in department_list:
                if department["id"] == department_id:
                    department_found = True
                    department_inspect = collegeapp.Departments(
                        department["name"],
                        department["description"],
                        department["id"],
                    )

            if department_inspect:
                manage_department_detail(department_inspect)
            else:
                print("No department member found")

        elif choice == "4":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_department_detail(department):
    while True:

        clear_screen()
        print(f"{department.name}\tdepartment ID: {department.id}")
        print(f"{department.description}")

        print("\nManage Department Menu")
        print("1) Update Department information")
        print("2) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # edit student  logic here
            clear_screen()
            print(f"{department.name}\tdepartment ID: {department.id}")
            print(f"{department.description}")
            updated_data = {
                "name": input(
                    "Please type updated Name or leave blank to leave unchanged: "
                ),
                "description": input(
                    "Please type updated description or leave blank to leave unchanged: "
                ),
            }

            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None
            status = department.update_department(
                update_push["name"],
                update_push["description"],
                department.id,
            )
            print(status)
            department.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_students():
    while True:
        clear_screen()
        command_mapping = {
            "gather_data": "get_students",
            "add": "add",
            "delete": "remove",
        }
        student_view = collegeapp.Student_views()
        student_attributes = ["id", "name", "email", "major"]
        display_columns = ["id ", "name", "email", "major"]
        manage_entities(
            "manage_entities",
            command_mapping,
            "student",
            collegeapp.Student_views,
            collegeapp.Students,
            student_attributes,
            display_columns,
        )


def manage_student_courses(student):
    while True:
        courses = {}
        courses = student.get_courses()
        enrolled_classes = []
        clear_screen()

        detailed_choices = [
            "course",
            {
                "get": "get_courses",
                "get_all": "get_all_courses",
                "add": "enroll",
                "remove": "withdraw",
            },
        ]
        print(f"{student.name}\tStudent ID: {student.id}")
        print(f"{student.email}\tMajor: {student.major} \n\nCurrently Enrolled")
        if courses:
            for course in courses:
                print(
                    f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                    f"{course['course_description']}\t Instructed by: {course['instructor_name']}\n",
                )

        print("\nManage student Menu")
        print("1) Update student information")
        print("2) Remove Class")
        print("3) Add Class")
        print("4) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # edit student  logic here
            clear_screen()
            print(f"{student.name}\tStudent ID: {student.id}")
            print(f"{student.email}\tMajor: {student.major} \n\nCurrently Enrolled")
            updated_data = {
                "name": input(
                    "Please type updated Name or leave blank to leave unchanged: "
                ),
                "email": input(
                    "Please type updated email or leave blank to leave unchanged: "
                ),
                "major": input(
                    "Please type updated major or leave blank to leave unchanged: "
                ),
            }
            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None

            status = student.update(
                update_push["name"],
                update_push["email"],
                update_push["major"],
                student.id,
            )
            print(status)
            student.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            clear_screen()
            print(f"{student.name}\tStudent ID: {student.id}")
            print(f"{student.email}\tMajor: {student.major} \n\nCurrently Enrolled")
            if courses:
                for course in courses:
                    print(
                        f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                        f"{course['course_description']}\t Instructed by: {course['instructor_name']}\n",
                    )

                x = input(
                    "Please enter Course ID to withdrawl from, leave blank to stop:  "
                )
                try:
                    course_id = int(x)
                    student.withdrawl(course_id)

                except:
                    continue

        elif choice == "3":
            # add class logic here
            clear_screen()
            print(f"{student.name}\tStudent ID: {student.id}")
            print(f"{student.email}\tMajor: {student.major} \n\nAvailable classes: ")
            views = collegeapp.Student_views()
            all_courses = views.get_all_courses()
            for course in all_courses:
                if course["course_id"] not in enrolled_classes:
                    print(
                        f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                        f"{course['course_description']}\t Instructed by: {course['instructor_name']}\n",
                    )

            add_course = []

            while True:
                x = input("Please enter Course ID to enroll, leave blank to stop:  ")
                if x == "":
                    break
                else:
                    add_course.append(x)

            for course_id_str in add_course:
                try:
                    course_id = int(course_id_str)
                    student.enroll(course_id)

                except ValueError:
                    pass

            student.get_courses()

        elif choice == "4":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_instructors():
    while True:
        clear_screen()
        instructor_view = collegeapp.Student_views()
        instructor_list = instructor_view.get_all_instructors()
        print("id\tname\temail\tDepartmend Name")
        for instructor in instructor_list:
            print(
                f"{instructor['id']}\t{instructor['name']}\t{instructor['email']}\t{instructor['department_name']}"
            )

        print("\nManage Instructors Menu")
        print("1) Add Instructor")
        print("2) Remove Instructor")
        print("3) View Instructors")
        print("4) Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add instructor logic here
            instructor_data = [
                input("Please enter the Instructor's Name: "),
                input("Please enter the Instructor's Email: "),
            ]
            clear_screen()
            departments = instructor_view.get_all_departments()
            for department in departments:
                print(
                    f"\n{department['id']}\t{department['name']}\t{department['description']}"
                )

            department_assigned = input("Please assign a department:  ")
            instructor = collegeapp.Instructors(
                instructor_data[0], instructor_data[1], department_assigned
            )

            status = instructor.add()
            print(status)
            input()
        elif choice == "2":
            # Remove instructor logic here
            instructor_id = input(
                "Please enter the Instructor ID you would like to remove: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                instructor_id = int(instructor_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            instructor_list = instructor_view.get_all_instructors()
            instructor_found = False

            for instructor in instructor_list:
                if instructor["id"] == instructor_id:
                    instructor_found = True
                    instructor_delete = collegeapp.Instructors(
                        instructor["name"],
                        instructor["email"],
                        instructor["department_id"],
                        instructor["id"],
                    )

                    clear_screen()
                    print(f"Instructor to delete: {instructor_delete.name}")

                    remove_choice = input(
                        "Remove the Instructor from the database? y/N "
                    ).strip()
                    if remove_choice.lower() == "y":
                        instructor_delete.remove()
                        print("Instructor removed successfully.")
                        input("Press Enter to continue...")
                    else:
                        print("Delete operation cancelled.")
                        input("Press Enter to continue...")
                    break  # Exit the loop once the student is found and action is taken

            if not instructor_found:
                print("Instructor with the given ID was not found.")
                input("Press Enter to continue...")

        elif choice == "3":
            # List instructors logic here
            instructor_id = input(
                "Please enter the Instructor ID you would like to view: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                instructor_id = int(instructor_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            instructor_list = instructor_view.get_all_instructors()
            instructor_found = False

            for instructor in instructor_list:
                if instructor["id"] == instructor_id:
                    instructor_found = True
                    instructor_inspect = collegeapp.Instructors(
                        instructor["name"],
                        instructor["email"],
                        instructor["department_id"],
                        instructor["id"],
                    )

                    clear_screen()

                    manage_instructor_courses(instructor_inspect)
        elif choice == "4":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_courses():
    while True:
        course_view = collegeapp.Student_views()
        courses = {}
        courses = course_view.get_courses_info()
        clear_screen()
        instructor_assigned = "No"

        if courses:
            for course in courses:
                if course["instructor_count"] > 0:
                    instructor_assigned = "Yes"

                print(
                    f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                    f"Students Enrolled: {course['student_count']}\t Professor assigned: {instructor_assigned}\n",
                    f"{course['course_description']}\n",
                )
        print("\nManage Courses Menu")
        print("1) Add Course")
        print("2) Remove Course")
        print("3) View Courses")
        print("4) Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add course logic here
            course_data = [
                input("Please enter the Course Name: "),
                input("Please enter the Course Description: "),
                input("Please enter the amount of Credits for this Course:  "),
            ]
            credits_int = None
            try:
                credits_int = int(course_data[2])
            except ValueError:
                print("Please enter an Integer for Credits")
                input()

            clear_screen()
            if credits_int:
                departments = course_view.get_all_departments()
                for department in departments:
                    print(
                        f"\n{department['id']}\t{department['name']}\t{department['description']}"
                    )

                department_assigned = input("Please assign a department:  ")
                new_course = collegeapp.Courses(
                    course_data[0], department_assigned, course_data[1], credits_int
                )

            status = new_course.add()
            print(status)
            input()

        elif choice == "2":
            # Remove course logic here
            course_id = input(
                "Please enter the Course ID you would like to remove: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                course_id = int(course_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            course_list = course_view.get_all_courses()
            course_found = False

            for course in course_list:
                if course["id"] == course_id:
                    course_found = True
                    course_delete = collegeapp.Courses(
                        course["name"],
                        course["department_id"],
                        course["description"],
                        course["credits"],
                        course["id"],
                    )

                    clear_screen()
                    print(f"Course to delete: {course_delete.name}")

                    remove_choice = input(
                        "Remove the Course from the database? y/N "
                    ).strip()
                    if remove_choice.lower() == "y":
                        course_delete.remove()
                        print("Course removed successfully.")
                        input("Press Enter to continue...")
                    else:
                        print("Delete operation cancelled.")
                        input("Press Enter to continue...")
                    break  # Exit the loop once the student is found and action is taken

            if not course_found:
                print("Course with the given ID was not found.")
                input("Press Enter to continue...")
            print("Remove Course selected")

        elif choice == "3":
            # List courses logic here
            course_id = input(
                "Please enter the Instructor ID you would like to view: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                course_id = int(course_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            course_list = course_view.get_all_courses()
            course_found = False
            course_inspect = None
            for course in course_list:
                if course["id"] == course_id:
                    course_found = True
                    course_inspect = collegeapp.Courses(
                        course["name"],
                        course["department_id"],
                        course["description"],
                        course["credits"],
                        course["id"],
                    )

            if course_inspect:
                manage_course_detail(course_inspect)
            else:
                print("No class found")

        elif choice == "4":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_course_detail(course):
    while True:

        clear_screen()
        department_name = course.get_department_name()
        print(f"{course.name}\tCourse ID: {course.id}\t Credits: {course.credits} ")
        print(f"{course.description}\nDepartment: {department_name[0]} ")

        print("\nManage Course Menu")
        print("1) Update Course information")
        print("2) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # edit student  logic here
            clear_screen()
            print(f"{course.name}\tCourse ID: {course.id}\t Credits: {course.credits}")
            print(f"{course.description}\nDepartment: {course.get_department_name()} ")
            updated_data = {
                "name": input(
                    "Please type updated Name or leave blank to leave unchanged: "
                ),
                "description": input(
                    "Please type updated description or leave blank to leave unchanged: "
                ),
                "credits": input(
                    "Please type updated Credits or leave blank to leave unchanged: "
                ),
            }
            try:
                credit_int = int(updated_data["credits"])
            except ValueError:
                credit_int = ""
            clear_screen()
            courses_view = collegeapp.Student_views()
            departments = courses_view.get_all_departments()
            for department in departments:
                print(
                    f"\n{department['id']}\t{department['name']}\t{department['description']}"
                )

            department_assigned = input(
                "Please assign a department or leave blank to skip:  "
            )
            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None

            if department_assigned == "":
                department_assigned = None

            status = course.update_course(
                update_push["name"],
                department_assigned,
                update_push["description"],
                credit_int,
                course.id,
            )
            print(status)
            course.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_instructor_courses(instructor):
    while True:
        courses = {}
        courses = instructor.get_courses()
        enrolled_classes = []
        clear_screen()
        print(f"{instructor.name}\tInstructor ID: {instructor.id}")
        print(
            f"{instructor.email}\tDepartment: {instructor.get_department_name()} \n\nCurrently Assigned Courses:"
        )
        if courses:
            for course in courses:
                print(
                    f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                    f"{course['course_description']}\n",
                )

        print("\nManage Instructor Menu")
        print("1) Update Instructor information")
        print("2) Unassign a Class")
        print("3) Assign a Class")
        print("4) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # edit student  logic here
            clear_screen()
            print(f"{instructor.name}\tInstructor ID: {instructor.id}")
            print(
                f"{instructor.email}\tDepartment: {instructor.get_department_name()} \n\nCurrently Assigned Courses:"
            )
            updated_data = {
                "name": input(
                    "Please type updated Name or leave blank to leave unchanged: "
                ),
                "email": input(
                    "Please type updated email or leave blank to leave unchanged: "
                ),
            }
            clear_screen()
            instructors_view = collegeapp.Student_views()
            departments = instructors_view.get_all_departments()
            for department in departments:
                print(
                    f"\n{department['id']}\t{department['name']}\t{department['description']}"
                )

            department_assigned = input(
                "Please assign a department or leave blank to skip:  "
            )
            if department_assigned == "":
                department_assigned = None
            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None

            status = instructor.update(
                update_push["name"],
                update_push["email"],
                department_assigned,
                instructor.id,
            )
            print(status)
            instructor.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            clear_screen()
            print(f"{instructor.name}\tInstructor ID: {instructor.id}")
            print(
                f"{instructor.email}\tDepartment: {instructor.get_department_name()} \n\nCurrently Assigned Courses:"
            )
            assigned_courses = instructor.get_assigned_courses()

            if assigned_courses:
                for course in assigned_courses:
                    print(
                        f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                        f"{course['course_description']}\n",
                    )

                x = input(
                    "Please enter Course ID to withdrawl from, leave blank to stop:  "
                )
                try:
                    course_id = int(x)
                    instructor.unassign(course_id)

                except:
                    continue

            instructor.get_courses()

        elif choice == "3":
            # add class logic here
            clear_screen()
            print(f"{instructor.name}\tInstructor ID: {instructor.id}")
            print(
                f"{instructor.email}\tDepartment: {instructor.get_department_name()} \n\nCurrently Assigned Courses:\n"
            )
            views = collegeapp.Student_views()
            all_courses = views.get_all_courses()
            for course in all_courses:
                if course["course_id"] not in enrolled_classes:
                    print(
                        f"ID: {course['course_id']}\t{course['course_name']}\tCredits: {course['course_credits']}\n",
                        f"{course['course_description']}\n",
                    )

            add_course = []

            while True:
                x = input("Please enter Course ID to assign, leave blank to stop:  ")
                if x == "":
                    break
                else:
                    add_course.append(x)

            for course_id_str in add_course:
                try:
                    course_id = int(course_id_str)
                    instructor.assign_course(course_id)

                except ValueError:
                    pass

            instructor.get_courses()

        elif choice == "4":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_staff():
    while True:
        staff_view = collegeapp.Student_views()
        staff_list = {}
        staff_list = staff_view.get_all_staff()
        clear_screen()

        if staff_list:
            for staff in staff_list:
                print(
                    f"ID: {staff['id']}\t Name: {staff['name']}\n",
                    f"Role: {staff['role']}\n",
                )

        print("\nManage Staff Menu")
        print("1) Add Staff")
        print("2) Remove Staff")
        print("3) View Staff")
        print("4) Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Add staff logic here
            staff_data = [
                input("Please enter Staff Name: "),
                input("Please enter Staff Role: "),
            ]

            clear_screen()

            new_staff = collegeapp.Staff(staff_data[0], staff_data[1])

            status = new_staff.add()
            print(status)
            input()

        elif choice == "2":
            # Remove staff logic here
            staff_id = input(
                "Please enter the Staff ID you would like to remove: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                staff_id = int(staff_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            staff_list = staff_view.get_all_staff()
            staff_found = False

            for staff in staff_list:
                if staff["id"] == staff_id:
                    staff_found = True
                    staff_delete = collegeapp.Staff(
                        staff["name"], staff["role"], staff["id"]
                    )

                    clear_screen()
                    print(f"Staff to delete: {staff_delete.name}")

                    remove_choice = input(
                        "Remove this Staff member from the database? y/N "
                    ).strip()
                    if remove_choice.lower() == "y":
                        staff_delete.remove()
                        print("staff removed successfully.")
                        input("Press Enter to continue...")
                    else:
                        print("Delete operation cancelled.")
                        input("Press Enter to continue...")
                    break  # Exit the loop once the student is found and action is taken

            if not staff_found:
                print("staff with the given ID was not found.")
                input("Press Enter to continue...")

        elif choice == "3":
            # List staff logic here
            staff_id = input(
                "Please enter the Staff ID you would like to view: "
            ).strip()

            # Convert input to integer and handle potential conversion error
            try:
                staff_id = int(staff_id)
            except ValueError:
                print("Invalid ID. Please enter a numeric value.")
                input("Press Enter to continue...")
                continue  # Restart the loop

            staff_list = staff_view.get_all_staff()
            staff_found = False
            staff_inspect = None
            for staff in staff_list:
                if staff["id"] == staff_id:
                    staff_found = True
                    staff_inspect = collegeapp.Staff(
                        staff["name"],
                        staff["role"],
                        staff["id"],
                    )

            if staff_inspect:
                manage_staff_detail(staff_inspect)
            else:
                print("No staff member found")

        elif choice == "4":
            print("Returning to the main menu...")
            break
        else:
            print("Invalid choice, please try again.")


def manage_staff_detail(staff):
    while True:

        clear_screen()
        print(f"{staff.name}\tStaff ID: {staff.id}")
        print(f"{staff.role}")

        print("\nManage Staff Menu")
        print("1) Update Staff member information")
        print("2) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # edit student  logic here
            clear_screen()
            print(f"{staff.name}\tStaff ID: {staff.id}")
            print(f"{staff.role}")
            updated_data = {
                "name": input(
                    "Please type updated Name or leave blank to leave unchanged: "
                ),
                "role": input(
                    "Please type updated role or leave blank to leave unchanged: "
                ),
            }

            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None
            status = staff.update_staff(
                update_push["name"],
                update_push["role"],
                staff.id,
            )
            print(status)
            staff.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


def exit_program():
    print("Exiting the program...")
    sys.exit(0)


def database_check():
    print("Checking for database access..")
    if os.path.isfile("college_data.db"):
        main_menu()
    else:
        db_create = input(
            "The file 'college_data.db' does not exist in the current directory. Would you like to create it? Y/n:  "
        )
        if db_create.capitalize() == "" or db_create.capitalize() == "Y":
            print("creating database file...")
            collegeapp.database_functions.initial_write("college_data.db")
            main_menu()
        else:
            input("Unable to continue without database. Press any key to exit.")
            exit_program()


def database_reset():

    os.remove("college_data.db")
    if os.path.isfile("college_data.db"):
        print("error, unable to delete database")
        input()
        exit_program()
    else:
        collegeapp.database_functions.initial_write("college_data.db")
        input("Database has been reset, Press Enter to continue")


def manage_entities(
    command,
    command_mapping,
    entity_name,
    entity_view_class,
    entity_class,
    attributes,
    display_columns,
    manage_related=None,
):
    if command == "manage_entities":
        if not all(
            [entity_name, entity_view_class, entity_class, attributes, display_columns]
        ):
            print("Missing required arguments for managing entities.")
            return

        while True:
            clear_screen()
            entity_view = entity_view_class()
            method_name = command_mapping.get(
                "gather_data", f"get_{entity_name.lower()}s"
            )
            entity_list = getattr(entity_view, method_name)()

            print("\t".join(display_columns))
            for entity in entity_list:
                print("\t".join(str(entity[attr]) for attr in attributes))

            print(f"\nManage {entity_name.capitalize()}s Menu")
            print(f"1) Add {entity_name.capitalize()}")
            print(f"2) Delete {entity_name.capitalize()} by ID")
            print(f"3) View {entity_name.capitalize()} by ID")
            print("4) Back to Main Menu")
            choice = input("Select an option: ").strip()

            if choice == "1":
                entity_data = []
                for attr in attributes:
                    if attr == "id":
                        continue
                    elif attr == "department_id":
                        department_id = get_department_choice(
                            entity_view.get_all_departments()
                        )
                        entity_data.append(department_id)
                    else:
                        entity_data.append(
                            input(
                                f"Please enter the {entity_name.capitalize()}'s {attr.capitalize()}: "
                            )
                        )

                entity = entity_class(*entity_data)
                add_method = getattr(entity, command_mapping.get("add", "add"))
                add_method()
                print(f"{entity_name.capitalize()} added successfully.")
                input("Press Enter to continue...")

            elif choice == "2":
                entity_id = input(
                    f"Please enter the {entity_name.capitalize()} ID you would like to delete: "
                ).strip()

                try:
                    entity_id = int(entity_id)
                except ValueError:
                    print("Invalid ID. Please enter a numeric value.")
                    input("Press Enter to continue...")
                    continue

                entity_found = False

                for entity in entity_list:
                    if entity["id"] == entity_id:
                        entity_found = True
                        entity_data = [
                            entity[attr] for attr in attributes if attr != "id"
                        ]
                        entity_data.append(entity["id"])
                        entity_instance = entity_class(*entity_data)
                        clear_screen()
                        print(
                            f"{entity_name.capitalize()} to delete: {entity_instance.name}"
                        )

                        remove_choice = input(
                            f"Delete the {entity_name.capitalize()} from the database? y/N "
                        ).strip()
                        if remove_choice.lower() == "y":
                            delete_method = getattr(
                                entity_instance, command_mapping.get("delete", "remove")
                            )
                            delete_method()
                            print(f"{entity_name.capitalize()} deleted successfully.")
                        else:
                            print("Delete operation cancelled.")
                        input("Press Enter to continue...")
                        break

                if not entity_found:
                    print(
                        f"{entity_name.capitalize()} with the given ID was not found."
                    )
                    input("Press Enter to continue...")

            elif choice == "3":
                entity_id = input(
                    f"Please enter the {entity_name.capitalize()} ID you would like to view: "
                ).strip()

                try:
                    entity_id = int(entity_id)
                except ValueError:
                    print("Invalid ID. Please enter a numeric value.")
                    input("Press Enter to continue...")
                    continue

                entity_found = False

                for entity in entity_list:
                    if entity["id"] == entity_id:
                        entity_found = True
                        entity_data = [
                            entity[attr] for attr in attributes if attr != "id"
                        ]
                        entity_data.append(entity["id"])
                        entity_instance = entity_class(*entity_data)

                        clear_screen()

                        if manage_related:
                            manage_related(entity_instance)
                        else:
                            print(
                                f"{entity_name.capitalize()} details: {entity_instance}"
                            )
                        input("Press Enter to continue...")

                if not entity_found:
                    print(
                        f"{entity_name.capitalize()} with the given ID was not found."
                    )
                    input("Press Enter to continue...")

            elif choice == "4":
                print("Returning to the main menu...")
                break
            else:
                print("Invalid choice, please try again.")
    else:
        print(f"Command '{command}' not recognized.")


def display_departments(departments):
    print("\nID\tName\tDescription")
    for department in departments:
        print(f"{department['id']}\t{department['name']}\t{department['description']}")


def get_department_choice(departments):
    while True:
        display_departments(departments)
        department_assigned = input(
            "Please assign a department by entering the ID or leave blank to skip: "
        ).strip()
        if department_assigned == "":
            return None

        # Convert input to integer and handle potential conversion error
        try:
            department_assigned = int(department_assigned)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            input("Press Enter to try again...")
            continue

        # Validate if the entered department ID exists
        for department in departments:
            if department["id"] == department_assigned:
                return department_assigned

        print("Department ID not found. Please enter a valid ID.")
        input("Press Enter to try again or leave blank to skip...")


def manage_detail_long(
    entity, entity_type, view_class, related_entity_name, related_entity_methods
):
    while True:
        related_entities = getattr(entity, related_entity_methods["get"])()
        enrolled_entities = []
        clear_screen()
        print(f"{entity.name}\t{entity_type.capitalize()} ID: {entity.id}")
        print(
            f"{entity.email}\t{related_entity_name.capitalize()}: {entity.major} \n\nCurrently Enrolled {related_entity_name.capitalize()}s"
        )
        if related_entities:
            for related_entity in related_entities:
                print(
                    f"ID: {related_entity['course_id']}\t{related_entity['course_name']}\tCredits: {related_entity['course_credits']}\n",
                    f"{related_entity['course_description']}\t Instructed by: {related_entity['instructor_name']}\n",
                )

        print(f"\nManage {entity_type.capitalize()} Menu")
        print(f"1) Update {entity_type} information")
        print(f"2) Remove {related_entity_name.capitalize()}")
        print(f"3) Add {related_entity_name.capitalize()}")
        print("4) Back to Previous Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            # Edit entity logic here
            clear_screen()
            print(f"{entity.name}\t{entity_type.capitalize()} ID: {entity.id}")
            print(
                f"{entity.email}\t{related_entity_name.capitalize()}: {entity.major} \n\nCurrently Enrolled {related_entity_name.capitalize()}s"
            )
            updated_data = {
                "name": input(
                    f"Please type updated Name or leave blank to leave unchanged: "
                ),
                "email": input(
                    f"Please type updated email or leave blank to leave unchanged: "
                ),
                "major": input(
                    f"Please type updated major or leave blank to leave unchanged: "
                ),
            }
            update_push = {}
            for key, value in updated_data.items():
                if value != "":
                    update_push[key] = value
                else:
                    update_push[key] = None

            status = entity.update(
                update_push["name"],
                update_push["email"],
                update_push["major"],
                entity.id,
            )
            print(status)
            entity.refresh()
            input("Press Enter to continue")

        elif choice == "2":
            clear_screen()
            print(f"{entity.name}\t{entity_type.capitalize()} ID: {entity.id}")
            print(
                f"{entity.email}\t{related_entity_name.capitalize()}: {entity.major} \n\nCurrently Enrolled {related_entity_name.capitalize()}s"
            )
            if related_entities:
                for related_entity in related_entities:
                    print(
                        f"ID: {related_entity['course_id']}\t{related_entity['course_name']}\tCredits: {related_entity['course_credits']}\n",
                        f"{related_entity['course_description']}\t Instructed by: {related_entity['instructor_name']}\n",
                    )

                x = input(
                    f"Please enter {related_entity_name.capitalize()} ID to withdraw, leave blank to stop: "
                )
                try:
                    related_entity_id = int(x)
                    getattr(entity, related_entity_methods["remove"])(related_entity_id)
                except ValueError:
                    continue

        elif choice == "3":
            # Add related entity logic here
            clear_screen()
            print(f"{entity.name}\t{entity_type.capitalize()} ID: {entity.id}")
            print(
                f"{entity.email}\t{related_entity_name.capitalize()}: {entity.major} \n\nAvailable {related_entity_name.capitalize()}s"
            )
            views = view_class()
            all_related_entities = getattr(views, related_entity_methods["get_all"])()
            for related_entity in all_related_entities:
                if related_entity["course_id"] not in enrolled_entities:
                    print(
                        f"ID: {related_entity['course_id']}\t{related_entity['course_name']}\tCredits: {related_entity['course_credits']}\n",
                        f"{related_entity['course_description']}\t Instructed by: {related_entity['instructor_name']}\n",
                    )

            add_related_entity = []

            while True:
                x = input(
                    f"Please enter {related_entity_name.capitalize()} ID to enroll, leave blank to stop: "
                )
                if x == "":
                    break
                else:
                    add_related_entity.append(x)

            for related_entity_id_str in add_related_entity:
                try:
                    related_entity_id = int(related_entity_id_str)
                    getattr(entity, related_entity_methods["add"])(related_entity_id)
                except ValueError:
                    pass

            getattr(entity, related_entity_methods["get"])()

        elif choice == "4":
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    database_check()
