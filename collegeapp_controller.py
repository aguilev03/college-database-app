import database_functions
import collegeapp


def grab(table):
    view_grab = collegeapp.Views()
    x = view_grab.get_table_data(table)
    return x


def process_student_schedule(student_data):
    student = collegeapp.Students(
        student_data["name"],
        student_data["email"],
        student_data["major"],
        student_data["id"],
    )
    print(student)
    courses = student.get_courses()
    course_data = []
    for course in courses:
        class_data = collegeapp.Courses(
            course[1], course[2], course[3], course[4], course[0]
        )
        course_data.append(course + class_data.get_instructor())

    print(course_data)

    return course_data
