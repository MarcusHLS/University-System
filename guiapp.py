import tkinter as tk
from tkinter import messagebox
import pickle
import re
import os
import traceback
from student import Subject

# === Constants ===
EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"
DATA_FILE = "students.data"

# === Load & Save Students Safely ===
def load_students():
    try:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "wb") as f:
                pickle.dump([], f)

        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError, FileNotFoundError, AttributeError) as e:
        print(f"Warning: Problem loading database ({e}). Loading empty students list.")
        return []

def save_students(students):
    try:
        with open(DATA_FILE, "wb") as f:
            pickle.dump(students, f)
    except Exception as e:
        print(f"Error saving students: {e}")

# === GUIUniApp Class ===
class GUIUniApp:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.master.title("GUIUniApp - Login")
        self.master.geometry("400x250")

        self.students = load_students()
        self.logged_in_student = None

        self.build_login_ui()

        self.poll_interval = 3000  # milliseconds
        self.start_polling_database()

    def start_polling_database(self):
        self.master.after(self.poll_interval, self.poll_database)

    def poll_database(self):
        updated_students = load_students()

        if self.logged_in_student:
            for s in updated_students:
                if s.email == self.logged_in_student.email:
                    self.logged_in_student = s
                    break

        self.students = updated_students

        if hasattr(self, "subject_listbox"):
            selected = self.subject_listbox.curselection()
            self.refresh_subject_list()
            if selected and selected[0] < self.subject_listbox.size():
                self.subject_listbox.select_set(selected[0])
                self.subject_listbox.activate(selected[0])
            self.status_label.config(
                text=f"You are enrolled in {len(self.logged_in_student.subject)} out of 4 subjects."
            )

        self.start_polling_database()

    def build_login_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("GUIUniApp - Login")

        tk.Label(self.master, text="Student Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.master, text="Email:").pack()
        self.email_entry = tk.Entry(self.master, width=30)
        self.email_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*", width=30)
        self.password_entry.pack()

        tk.Button(self.master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and password cannot be empty")
            return

        if not re.fullmatch(EMAIL_PATTERN, email) or not re.fullmatch(PASSWORD_PATTERN, password):
            messagebox.showerror("Error", "Invalid email or password format")
            return

        for student in self.students:
            if student.email == email and student.password == password:
                self.logged_in_student = student
                messagebox.showinfo("Success", f"Welcome {student.name}!")
                self.build_enrolment_ui()
                return

        messagebox.showerror("Error", "Student not found or incorrect password")

    def build_enrolment_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("GUIUniApp - Enrolment")

        tk.Label(self.master, text=f"Welcome {self.logged_in_student.name}", font=("Arial", 14)).pack(pady=10)
        self.status_label = tk.Label(
            self.master, 
            text=f"You are enrolled in {len(self.logged_in_student.subject)} out of 4 subjects."
        )
        self.status_label.pack()

        tk.Button(self.master, text="Enrol in a new subject", command=self.enrol_subject).pack(pady=5)
        tk.Button(self.master, text="Go to My Subjects", command=self.open_subject_window).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.confirm_logout).pack(pady=5)

    def enrol_subject(self):
        if len(self.logged_in_student.subject) >= 4:
            messagebox.showwarning("Limit Reached", "You can only enrol in 4 subjects.")
            return

        subject = Subject()
        self.logged_in_student.subject.append(subject)
        self.logged_in_student.update_mark()
        self.logged_in_student.update_grade()
        save_students(self.students)
        messagebox.showinfo("Success", f"Enrolled in Subject {subject.id}")
        self.status_label.config(text=f"You are enrolled in {len(self.logged_in_student.subject)} out of 4 subjects.")

    def open_subject_window(self):
        SubjectWindow(self.master, self.logged_in_student, self.students)

    def confirm_logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            save_students(self.students)
            self.build_login_ui()

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            save_students(self.students)
            self.master.destroy()

    def refresh_subject_list(self):
        if hasattr(self, "subject_listbox"):
            self.subject_listbox.delete(0, tk.END)
            for sub in self.logged_in_student.subject:
                self.subject_listbox.insert(tk.END, f"Subject ID: {sub.id}, Mark: {sub.mark}, Grade: {sub.grade}")

# === New SubjectWindow Class ===
class SubjectWindow:
    def __init__(self, parent, student, all_students):
        self.top = tk.Toplevel(parent)
        self.top.title("My Subjects")
        self.top.geometry("450x300")

        self.student = student
        self.all_students = all_students

        tk.Label(self.top, text="Your Enrolled Subjects", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(self.top, width=50)
        self.listbox.pack(pady=10)
        self.refresh_list()

        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="View Details", command=self.view_subject).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_subject).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=self.top.destroy).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for sub in self.student.subject:
            self.listbox.insert(tk.END, f"Subject ID: {sub.id}, Mark: {sub.mark}, Grade: {sub.grade}")

    def view_subject(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a subject.")
            return
        sub = self.student.subject[selected[0]]

        detail = tk.Toplevel(self.top)
        detail.title("Subject Details")
        detail.geometry("300x150")
        tk.Label(detail, text=f"Subject ID: {sub.id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detail, text=f"Mark: {sub.mark}", font=("Arial", 12)).pack(pady=5)
        tk.Label(detail, text=f"Grade: {sub.grade}", font=("Arial", 12)).pack(pady=5)
        tk.Button(detail, text="Close", command=detail.destroy).pack(pady=10)

    def remove_subject(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a subject to remove.")
            return

        sub = self.student.subject[selected[0]]
        confirm = messagebox.askyesno("Confirm", f"Remove Subject {sub.id}?")
        if confirm:
            self.student.subject.pop(selected[0])
            self.student.update_mark()
            self.student.update_grade()
            save_students(self.all_students)
            self.refresh_list()

