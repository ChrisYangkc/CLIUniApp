import tkinter as tk
from tkinter import messagebox
from controllers import StudentControllerGUI
from validators import validate_email, validate_password
from models import Subject

class GUIUniApp:
    # A graphical user interface for the university application.
    def __init__(self, master):
        # Initializes the GUIUniApp with the main window.
        self.master = master
        self.master.title("GUIUniApp")
        
        self.master.geometry("600x400")  # Set initial window size
        
        self.frame = tk.Frame(self.master)  # Add a frame to hold widgets
        self.frame.pack(pady=50, expand=True)
        
        self.student_controller = StudentControllerGUI()
        
        self.create_login_widgets()

    def create_login_widgets(self):
        # Creates and sets up widgets related to the login functionality.
        self.clear_widgets()
        
        tk.Label(self.frame, text="Student Login", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.frame, text="Email:").pack(anchor='w', padx=50)
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.pack(fill=tk.X, padx=50, pady=5)
        
        tk.Label(self.frame, text="Password:").pack(anchor='w', padx=50)
        self.password_entry = tk.Entry(self.frame, show="*", width=30)
        self.password_entry.pack(fill=tk.X, padx=50, pady=5)
        
        tk.Button(self.frame, text="Login", command=self.login).pack(pady=20)

    def create_enrollment_widgets(self, window):
        # Creates and sets up widgets related to student enrollment functionalities.
        self.frame = tk.Frame(window)  # Create a new frame in the new window
        self.frame.pack(pady=50, expand=True)
        
        tk.Label(self.frame, text="Enrolment Management", font=("Arial", 20)).pack(pady=10)
        tk.Button(self.frame, text="Enroll in a Subject", command=self.enroll_subject).pack(pady=10)
        tk.Button(self.frame, text="Show Subjects", command=self.show_enrollment).pack(pady=10)
        tk.Button(self.frame, text="Logout", command=window.destroy).pack(pady=20)  # Close the new window when logout

    
    def login(self):
        # Validates and logs in a student using the provided email and password.
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            # Check if email or password fields are empty
            messagebox.showerror("Error", "Fields cannot be empty!")
            return

        if not validate_email(email):
            # Validate the format of the email
            messagebox.showerror("Error", "Invalid email format!")
            return
            
        if not validate_password(password):
            # Validate the format of the password
            messagebox.showerror("Error", "Invalid password format!")
            return

        if self.student_controller.login(email, password):
            self.enroll_win = tk.Toplevel(self.master)  # Create a new window for enrolment management
            self.enroll_win.title("Enrolment Management")
            self.enroll_win.geometry("600x400")
            self.create_enrollment_widgets(self.enroll_win)
            self.clear_login_input()
        else:
            messagebox.showerror("Error", "Incorrect credentials!")

    def enroll_subject(self):
        # Enroll the student in a subject.
        if len(self.student_controller.current_student.subjects) >= 4:
            messagebox.showinfo("Info", "You are already enrolled in the maximum number of subjects.")
            return

        subject = Subject()  # This part might require modification as per how Subjects are added
        self.student_controller.enroll_subject(subject)
        messagebox.showinfo("Success", "Subject enrolled!")

    def clear_widgets(self):
        # Clears all widgets from the current frame.
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show_enrollment(self):
        # Display the subjects in which the student is currently enrolled.
        subjects = self.student_controller.current_student.subjects

        # Create a new Toplevel window
        enroll_win = tk.Toplevel(self.master)
        enroll_win.title("Your Enrolled Subjects")
        enroll_win.geometry("600x400")

        # Create a frame inside the window for better organization of widgets
        frame = tk.Frame(enroll_win)
        frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)

        # Title label
        tk.Label(frame, text="Enrolment Management", font=("Arial", 20)).pack(pady=10)
        label_width = 60  # Adjust as needed
        subject_font = ("Times New Roman", 12)
        # Display subjects in the frame
        if not subjects:
            tk.Label(frame, text="You haven't enrolled in any subjects.", font=subject_font, width=label_width, anchor='center', justify='center').pack(pady=10)
        else:
            for sub in subjects:
                subject_info = f"Subject: {sub.ID}, Mark: {sub.mark}, Grade: {sub.grade}"
                tk.Label(frame,text=subject_info, font=subject_font, width=label_width, anchor='center', justify='center').pack(pady=5, side='top')

        # Add a close button
        tk.Button(frame, text="Close", command=enroll_win.destroy).pack(pady=20)

    def clear_login_input(self):
        # Clear the email and password fields in the login form.
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)



# Launch the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIUniApp(master=root)
    root.mainloop()
