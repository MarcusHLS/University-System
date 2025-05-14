import tkinter as tk
from tkinter import messagebox
from controller.student_controller import StudentController
from controller.subject_controller import SubjectController
from model.database import Database
import re

class GUIUniApp:
    def __init__(self, master):
        self.master = master
        
        self.master.title("University System")
        self.master.geometry("400x300")
        
        self.student_controller = StudentController()
        self.subject_controller = SubjectController(self.student_controller.students)
        
        self.students = Database.load_students()
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
        tk.Button(self.master, text="Register", command=self.register).pack(pady=5)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        student, message = self.student_controller.login(email, password)
        message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
        messagebox.showinfo("Login", message)
        
        if student:
            self.logged_in_student = student
            self.build_student_menu()

    def register(self):
        reg_window = tk.Toplevel(self.master)
        reg_window.title("Register")
        
        tk.Label(reg_window, text="Name:").pack()
        name_entry = tk.Entry(reg_window)
        name_entry.pack()
        
        tk.Label(reg_window, text="Email:").pack()
        email_entry = tk.Entry(reg_window)
        email_entry.pack()
        
        tk.Label(reg_window, text="Password:").pack()
        password_entry = tk.Entry(reg_window, show="*")
        password_entry.pack()
        
        def do_register():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            _, message = self.student_controller.register(name, email, password)
            message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
            messagebox.showinfo("Register", message)
            self.students = Database.load_students()
            reg_window.destroy()

        tk.Button(reg_window, text="Register", command=do_register).pack(pady=5)

    def build_student_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Welcome {self.logged_in_student.name}").pack(pady=10)

        tk.Button(self.master, text="Enrol Subject", command=self.enrol_subject).pack(pady=5)
        tk.Button(self.master, text="Show Subjects", command=self.show_subjects).pack(pady=5)
        tk.Button(self.master, text="Remove Subjects", command=self.remove_subjects).pack(pady=5)
        tk.Button(self.master, text="Change Password", command=self.change_password).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=5)

    def enrol_subject(self):
        message = self.subject_controller.enrol_subject(self.logged_in_student)
        message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
        messagebox.showinfo("Enrol Subject", message)

    def show_subjects(self):
        message = self.subject_controller.get_subjects(self.logged_in_student)
        message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
        messagebox.showinfo("Subjects", message)

    def remove_subjects(self):
        rev_window = tk.Toplevel(self.master)
        rev_window.title("Register")
        
        tk.Label(rev_window, text="Enter Subject's ID:").pack()
        id_entry = tk.Entry(rev_window)
        id_entry.pack()
        
        def do_remove():
            id = id_entry.get().strip()
            
            message = self.subject_controller.remove_subject(self.logged_in_student, id)
            message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
            messagebox.showinfo("Remove Subject by ID", message)
            self.sync_logged_in_student()
            rev_window.destroy()

        tk.Button(rev_window, text="Remove", command=do_remove).pack(pady=5)

    def change_password(self):
        change_password_window = tk.Toplevel(self.master)
        change_password_window.title("Change Password")
        
        tk.Label(change_password_window, text="Enter new password:").pack()
        new_password_entry = tk.Entry(change_password_window)
        new_password_entry.pack()

        tk.Label(change_password_window, text="Enter confirm password:").pack()
        confirm_password_entry = tk.Entry(change_password_window)
        confirm_password_entry.pack()
        
        def do_change():
            new_password = new_password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()
            message = self.student_controller.change_password(self.logged_in_student, new_password, confirm_password)
            message = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', message).strip()
            messagebox.showinfo("Change Account Password", message)
            self.sync_logged_in_student()
            change_password_window.destroy()

        tk.Button(change_password_window, text="Change Password", command=do_change).pack(pady=5)

    def logout(self):
        self.student_controller.save_students()
        self.logged_in_student = None
        self.build_login_ui()

    def sync_logged_in_student(self):
        self.students = Database.load_students()
        for student in self.students:
            if student.email == self.logged_in_student.email:
                self.logged_in_student = student
                break
