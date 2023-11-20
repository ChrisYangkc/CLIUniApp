from controllers import StudentController, AdminController

def main_menu():
    # main menu
    while True:
        choice = input("\033[38;2;21;189;208mUniversity System: (A)dmin, (S)tudent, or X : \033[0m").lower()

        if choice == 'a':
            admin_menu()
        elif choice == 's':
            student_menu()
        elif choice == 'x':
            print("\033[93mThank You \033[0m")
            break
        else:
            print("\033[91mInvalid choice. Please try again. \033[0m")


def student_menu():
    # Student Menu
    student_controller = StudentController()

    while True:
        choice = input("\033[38;2;21;189;208m\tStudent System (l/r/x): \033[0m").lower()

        if choice == 'l':    
            if student_controller.login():
                student_course_menu(student_controller)    
        elif choice == 'r':
            student_controller.register()
        elif choice == 'x':
            break
        else:
            print("\033[91m\tInvalid choice. Please try again. \033[0m")


def student_course_menu(controller):
    # Student Course Selection Menu
    while True:
        choice = input("\033[38;2;21;189;208m\t\tStudent Course Menu (c/e/r/s/x): \033[0m").lower()

        if choice == 'c':
            controller.change_password()

        elif choice == 'e':
            controller.enroll_subject()

        elif choice == 'r':
            subject_id = input("\t\tRemove Subject by ID: ")
            controller.remove_subject(subject_id)

        elif choice == 's':
            controller.show_enrollment()

        elif choice == 'x':
            break
        else:
            print("\033[91m\t\tInvalid choice. Please try again. \033[0m")


def admin_menu():
    # Administrator Menu
    admin_controller = AdminController()

    while True:
        choice = input("\033[38;2;21;189;208m\tAdmin System (c/g/p/r/s/x): \033[0m").lower()

        if choice == 'c':
            admin_controller.clear_database()

        elif choice == 'g':
            admin_controller.group_students_by_grade()

        elif choice == 'p':
            admin_controller.partition_students()

        elif choice == 'r':
            student_id = input("\tRemove by ID: ")
            admin_controller.remove_student(student_id)

        elif choice == 's':
            admin_controller.show_all_students()

        elif choice == 'x':
            break
        else:
            print("\033[91m\tInvalid choice. Please try again. \033[0m")


if __name__ == "__main__":
    main_menu()
