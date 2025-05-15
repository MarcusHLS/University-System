import tkinter as tk
from tkinter import messagebox
from controller.student_controller import StudentController
from controller.subject_controller import SubjectController
import re

class GUIUniApp:
    def __init__(self, master):
        self.master = master
        self.master.title("University System")
        self.master.geometry("400x300")

        self.student_controller = StudentController()
        self.subject_controller = SubjectController()
        self.logged_in_student = None

        self.build_login_ui()

    def build_login_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Student Login").pack(pady=10)

        tk.Label(self.master, text="Email:").pack()
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        tk.Button(self.master, text="Login", command=self.login).pack(pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        student = self.student_controller.login(email, password)
        if student:
            self.logged_in_student = student
            messagebox.showinfo("Login", f"Welcome {student.name}")
            self.build_student_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def build_student_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Welcome {self.logged_in_student.name}").pack(pady=10)

        tk.Button(self.master, text="Enrol Subject", command=self.enrol_subject).pack(pady=5)
        tk.Button(self.master, text="Show Subjects", command=self.show_subjects).pack(pady=5)
        tk.Button(self.master, text="Remove Subject", command=self.remove_subject).pack(pady=5)
        tk.Button(self.master, text="Change Password", command=self.change_password).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=5)

    def enrol_subject(self):
        subject = self.subject_controller.enrol_subject(self.logged_in_student)
        if subject:
            messagebox.showinfo("Enrolled", f"Enrolled subject {subject.id} | Mark: {subject.mark} | Grade: {subject.grade}")
        else:
            messagebox.showwarning("Limit Reached", "You can enrol in up to 4 subjects.")

    def show_subjects(self):
        subjects = self.subject_controller.show_subjects(self.logged_in_student)
        if not subjects:
            messagebox.showinfo("Subjects", "No enrolled subjects.")
            return
        info = "\n".join([f"ID: {s.id} | Mark: {s.mark:3} | Grade: {s.grade}" for s in subjects])
        messagebox.showinfo("Subjects", info)

    def remove_subject(self):
        remove_window = tk.Toplevel(self.master)
        remove_window.title("Remove Subject")

        tk.Label(remove_window, text="Enter Subject ID to remove:").pack()
        subject_id_entry = tk.Entry(remove_window)
        subject_id_entry.pack()

        def do_remove():
            subject_id = subject_id_entry.get().strip()
            success = self.subject_controller.remove_subject(self.logged_in_student, subject_id)
            if success:
                messagebox.showinfo("Removed", f"Subject {subject_id} removed.")
            else:
                messagebox.showerror("Error", "Subject not found.")
            remove_window.destroy()

        tk.Button(remove_window, text="Remove", command=do_remove).pack(pady=5)

    def change_password(self):
        pw_window = tk.Toplevel(self.master)
        pw_window.title("Change Password")

        tk.Label(pw_window, text="New Password:").pack()
        new_pw_entry = tk.Entry(pw_window, show="*")
        new_pw_entry.pack()

        tk.Label(pw_window, text="Confirm Password:").pack()
        confirm_pw_entry = tk.Entry(pw_window, show="*")
        confirm_pw_entry.pack()

        def do_change():
            new_pw = new_pw_entry.get().strip()
            confirm_pw = confirm_pw_entry.get().strip()
            result = self.student_controller.change_password(self.logged_in_student, new_pw, confirm_pw)

            if result == "changed":
                messagebox.showinfo("Success", "Password updated.")
            elif result == "mismatch":
                messagebox.showerror("Error", "Passwords do not match.")
            elif result == "invalid_format":
                messagebox.showerror("Error", "Invalid password format.")

            pw_window.destroy()

        tk.Button(pw_window, text="Change", command=do_change).pack(pady=5)

    def logout(self):
        self.logged_in_student = None
        self.build_login_ui()
