from models import Student, Subject, Database
from validators import validate_email, validate_password

class StudentController:
    def __init__(self):
        #Initialize the class with a Database instance and set the current student to None.
        self.db = Database()
        self.current_student = None
        
    def register(self):
        # Register a new student.

        # The method prompts the user to input an email and password. 
        # It then checks if the email and password are in the correct format 
        # using the validate_email and validate_password functions.
        
        # If the provided email already exists in the database, the registration is stopped. 
        # Otherwise, the method continues to prompt for the student's name and saves the new student to the database.
        print("\033[38;2;40;214;56m\tStudent Sign Up \033[0m")
        while True:
            email = input("\tEmail: ")
            password = input("\tPassword: ")

            if not validate_email(email) or not validate_password(password):
                print('\033[91m\tIncorrect email or password format \033[0m')
                continue
            print("\033[93m\temail and password formats acceptable \033[0m")
            students = self.db.read_from_file()
            if any(student.email == email for student in students):
                print(f"\033[91m\tStudent {email.split('@')[0].replace('.', ' ').title()} already exists \033[0m")
                break
            
            name = input("\tName: ")
            new_student = Student(name, email, password)
            students.append(new_student)
            self.db.write_to_file(students)
            print(f"\033[93m\tEnrolling Student {name} \033[0m")
            break

    def login(self):
        # Authenticate a student using their email and password.
        print("\033[38;2;40;214;56m\tStudent Sign In \033[0m")
        while True:
            email = input("\tEmail: ")
            password = input("\tPassword: ")

            # Verification Email and Password Format
            if not validate_email(email) or not validate_password(password):
                print("\033[91m\tIncorrect email or password format \033[0m")
                continue
            
            print("\033[93m\temail and password formats acceptable \033[0m")
            
            students = self.db.read_from_file()
            for student in students:
                if student.email == email and student.password == password:
                    self.current_student = student
                    return True
            
            # If the student is not found
            print("\033[91m\tStudent does not exist \033[0m")
            break


    def enroll_subject(self):
        # Enroll the current student in a new subject.
        subject = Subject()
        # Create a new subject instance.
        self.current_student.add_subject(subject)
        self.update_student_data()
        

    def remove_subject(self, subject_id):
        # Remove a subject from the current student's list of subjects based on its ID.
        self.current_student.remove_subject(subject_id)
        self.update_student_data()
        print(f"\033[93m\t\tDroping Subject-{subject_id} \033[0m")
        print(f"\033[93m\t\tYou are now enrolled in {len(self.current_student.subjects)} out of 4 subjects \033[0m")

    def change_password(self):
        # Change the password of the current student.
        print("\033[93m\t\tUpdating Password \033[0m")
        new_password = input("\t\tNew Password: ")
        
        while True:
            confirm_password = input("\t\tConfirm Password: ")
            if new_password == confirm_password:
                self.current_student.change_password(new_password)
                self.update_student_data()
                break
            else:
                print("\033[91m\t\tPassword does not match - try again \033[0m")

    def show_enrollment(self):
        # Display the subjects in which the current student is enrolled.
        subjects = self.current_student.subjects
        print(f"\033[93m\t\tShowing {len(subjects)} subjects \033[0m")
        for sub in subjects:
            print(f"\t\t[ Subject::{sub.ID:>3} -- mark = {sub.mark:>2} -- grade =  {sub.grade:>2} ]")

    def update_student_data(self):
        # Update the current student's data in the database.
        students = self.db.read_from_file()
        for i, student in enumerate(students):
            if student.email == self.current_student.email:
                students[i] = self.current_student
                break
        self.db.write_to_file(students)

class AdminController:
    def __init__(self):
        self.db = Database()

    def clear_database(self):
        # Clear the entire student database.
        print("\033[93m\tCLearing students database\033[0m")
        choice = input("\033[91m\tAre you sure you want to clear the database (Y)ES/(N)O : \033[0m").lower()
        if choice == 'y':
            print("\033[93m\tStudents data cleared \033[0m")
            self.db.clear_file()
        elif choice == 'n':
            return

    def group_students_by_grade(self):
        # Group students by their average grade and display the results.
        print("\033[93m\tGrade Grouping \033[0m")
        students = self.db.read_from_file()
        grade_groups = {}
        if not students:
            print("\t\t< Nothing to Display >")
        else:
            for student in students:
                total_marks = 0
                subject_count = len(student.subjects)

                # Calculate the student's average score in all subjects
                for subject in student.subjects:
                    total_marks += subject.mark

                avg_mark = total_marks / subject_count if subject_count != 0 else 0
                grade = Subject.calculate_grade(avg_mark)

                # Group students according to the level of their average score
                if grade not in grade_groups:
                    grade_groups[grade] = []
                grade_groups[grade].append({
                    'name': student.name,
                    'id': student.ID,
                    'avg_mark': avg_mark,
                    'grade': grade
                })

            for grade, students_list in grade_groups.items():
                print(f"\t{grade} --> [", end='')
                for student in students_list:
                    if student['avg_mark']>0:
                        print(f"{student['name']:<10} :: {student['id']:>6} --> GRADE: {student['grade']:>2} - MARK: {student['avg_mark']:<5.2f}", end='')
                print(']')
                
            return grade_groups

    def partition_students(self):
        # Partition students into 'pass' and 'fail' lists based on average grade.
        students = self.db.read_from_file()
        pass_list = []
        fail_list = []

        for student in students:
            total_marks = 0
            subject_count = len(student.subjects)
            # Calculate the student's average score in all subjects
            for subject in student.subjects:
                total_marks += subject.mark

            avg_mark = total_marks / subject_count if subject_count != 0 else 0
            grade = Subject.calculate_grade(avg_mark)

            student_info = f"{student.name:<10} :: {student.ID:>6} --> GRADE: {grade:>2} - MARK: {avg_mark:<5.2f}"
            
            if avg_mark >= 50:
                pass_list.append(student_info)
            elif 50> avg_mark > 0:
                fail_list.append(student_info)
        print("\033[93m\tPASS/FAIL Partition \033[0m")
        print("\tFAIL --> ["+ ', '.join(fail_list)+"]")
        print("\tPASS --> ["+ ', '.join(pass_list)+"]")

    def remove_student(self, student_id):
        # Remove a student based on their student ID.
        students = self.db.read_from_file()

        # Find out if there is a matching student ID
        matching_students = [s for s in students if s.ID == student_id]

        if not matching_students:
            # If there are no matching students, print an error message
            print(f"\033[91m\tStudent {student_id} does not exist \033[0m")
            return

        # If there are matches, delete them
        students = [s for s in students if s.ID != student_id]
        self.db.write_to_file(students)
        print(f"\033[93m\tRemoving Student {student_id} Account \033[0m")


    def show_all_students(self):
        # Display a list of all students in the database.
        print("\033[93m\tStudent List \033[0m")
        students = self.db.read_from_file()
        if not students:
            print("\t\t< Nothing to Display >")
        else:
            for student in students:
                print(f"\t{student.name:<10} :: {student.ID:>6} --> Email: {student.email}")


class StudentControllerGUI:
    # Represents a controller for managing student operations in a GUI environment.
    def __init__(self):
        # Initialize an instance of the StudentControllerGUI class.
        self.db = Database()
        self.current_student = None

    def register(self, email, password, name=None):
        # Register a new student using the provided email, password, and name.
        if not validate_email(email) or not validate_password(password):
            return False

        students = self.db.read_from_file()
        if any(student.email == email for student in students):
            return False

        if not name:
            return False

        new_student = Student(name, email, password)
        students.append(new_student)
        self.db.write_to_file(students)
        return True

    def login(self, email, password):
        # Attempt to log a student in using the provided email and password.
        if not validate_email(email) or not validate_password(password):
            return False

        students = self.db.read_from_file()
        for student in students:
            if student.email == email and student.password == password:
                self.current_student = student
                return True
        return False

    def enroll_subject(self, subject):
        # Assuming subject is an instance of Subject or equivalent data
        self.current_student.add_subject(subject)
        self.update_student_data()
        return True
    
    def show_enrollment(self):
        # Retrieves the current student's subject enrollment.
        subjects = self.current_student.subjects
        subject_info = []
        for sub in subjects:
            subject_info.append(f"[ Subject:{sub.ID} -- mark = {sub.mark} -- grade = {sub.grade} ]")
        return subject_info

    def update_student_data(self):
        # Updates the current student's data in the database.
        students = self.db.read_from_file()
        for i, student in enumerate(students):
            if student.email == self.current_student.email:
                students[i] = self.current_student
                break
        self.db.write_to_file(students)


