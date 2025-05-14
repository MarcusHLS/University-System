import tkinter as tk
from tkinter import messagebox
from controller.student_controller import StudentController
from controller.subject_controller import SubjectController

class GUIUniApp:
    def __init__(self):
        self.controller = StudentController()
        self.subject_controller = SubjectController()
        self.student = None
        self.root = tk.Tk()
        self.root.title("GUIUniApp - Login")
        self.login_window()

    def login_window(self):
        self.clear_window()

        tk.Label(self.root, text="Email:").grid(row=0, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_btn = tk.Button(self.root, text="Login", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Email and Password cannot be empty.")
            return

        if not self.controller.validate_credentials(email, password):
            messagebox.showerror("Error", "Invalid email or password format.")
            return

        student = self.controller.login(email, password)
        if student:
            self.student = student
            self.enrolment_window()
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password.")

    def enrolment_window(self):
        self.clear_window()
        self.root.title("Enrolment Window")

        tk.Label(self.root, text=f"Welcome {self.student.name}", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        self.subject_listbox = tk.Listbox(self.root, width=50)
        self.subject_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.refresh_subject_list()

        tk.Button(self.root, text="Enrol in New Subject", command=self.enrol_subject).grid(row=2, column=0, pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).grid(row=2, column=1, pady=10)

    def enrol_subject(self):
        if len(self.student.subjects) >= 4:
            messagebox.showwarning("Limit Reached", "You can only enrol in up to 4 subjects.")
            return

        subject = self.subject_controller.enrol_subject(self.student)
        messagebox.showinfo("Enrolled", f"Subject {subject.id} enrolled with mark {subject.mark} and grade {subject.grade}")
        self.refresh_subject_list()

    def refresh_subject_list(self):
        self.subject_listbox.delete(0, tk.END)
        for subj in self.student.subjects:
            self.subject_listbox.insert(tk.END, f"Subject {subj.id} | Mark: {subj.mark} | Grade: {subj.grade}")

    def logout(self):
        self.student = None
        self.login_window()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GUIUniApp()
    app.run()

