import os
import pickle
import random

class Student:
    # Represents a student with attributes for identification, name, email, password, and subjects.
    def __init__(self, name, email, password):
        # Initialize the student with the given name, email, and password, and generate a unique ID.
        self.ID = self.generate_id(999999, 6)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []# empty list

    def generate_id(self, max_value, width):
        # Generate a random unique ID for a student with a specified width.
        id_val = str(random.randint(1, max_value))
        return id_val.zfill(width)

    def add_subject(self, subject):
        # Enroll the student in a new subject.    
        # If the student is already enrolled in 4 subjects, they cannot enroll in additional subjects.
        if len(self.subjects) < 4:
            self.subjects.append(subject)
            print(f"\033[93m\t\tEnrolling in Subject-{subject.ID}  \033[0m")
            print(f"\033[93m\t\tYou are now enrolled in {len(self.subjects)} out of 4 subjects  \033[0m")
        else:
            print("\033[91m\t\tStudent are allowed to enrol in 4 subjects only \033[0m")

    def remove_subject(self, subject_id):
        # Remove a subject from the student's list of enrolled subjects based on its ID.
        self.subjects = [sub for sub in self.subjects if sub.ID != subject_id]

    def change_password(self, new_password):
        # Change the student's password to a new value.
        self.password = new_password


class Subject:
    # Represents an academic subject with attributes for identification, mark, and grade.
    def __init__(self):
        # Initialize the subject with a unique ID, a randomly assigned mark, and a corresponding grade.
        self.ID = self.generate_id(999, 3)
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade(self.mark)

    def generate_id(self, max_value, width):
        # Generate a random unique ID for the subject with a specified width.
        id_val = str(random.randint(1, max_value))
        return id_val.zfill(width)

    @staticmethod
    def calculate_grade(mark):
        # Calculate the grade based on the given mark.
        if mark >= 85:
            return "HD"
        elif mark >= 75:
            return "D"
        elif mark >= 65:
            return "C"
        elif mark >= 50:
            return "P"
        else:
            return "Z"

class Database:
    # Represents a simple database for storing and retrieving data in a file using pickle.
    def __init__(self, filename="students.data"):
        # Initialize the database with a specified filename or a default name.
        self.filename = filename

    def file_exists(self):
        # Check if the data file exists.
        return os.path.exists(self.filename)

    def create_file(self):
        # Create a new data file or overwrite an existing one with an empty list.
        with open(self.filename, 'wb') as file:
            pickle.dump([], file)

    def write_to_file(self, data):
        # Store the given data in the data file.
        with open(self.filename, 'wb') as file:
            pickle.dump(data, file)

    def read_from_file(self):
        # Read and return the data from the data file. 
        # If the file doesn't exist, it gets created.
        if not self.file_exists():
            self.create_file()
        with open(self.filename, 'rb') as file:
            return pickle.load(file)

    def clear_file(self):
        # Clear the contents of the data file by overwriting it with an empty list.
        self.create_file()
