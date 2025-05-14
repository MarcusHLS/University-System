from model.student import Student
from model.database import Database
import re

EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def login(self, email, password):
        Database.load_students()
        if not (re.fullmatch(EMAIL_PATTERN, email) and re.fullmatch(PASSWORD_PATTERN, password)):
            return None, "\n\t\033[31mInvalid email or password format.\033[0m"
        for student in self.students:
            if student.email == email and student.password == password:
                return student, f"\n\t\t\033[36mWelcome back, {student.name}!\033[0m"
        return None, "\n\t\033[31mStudent not found or incorrect password.\033[0m"

    def register(self, name, email, password):
        Database.load_students()
        if not re.fullmatch(EMAIL_PATTERN, email):
            return None, "\n\t\033[31mInvalid email format.\033[0m"
        if not re.fullmatch(PASSWORD_PATTERN, password):
            return None, "\n\t\033[31mInvalid password format.\033[0m"
        if any(s.email == email for s in self.students):
            return None, f"\n\t\033[31mStudent with email {email} already exists.\033[0m"

        new_student = Student(name, email, password)
        self.students.append(new_student)
        Database.save_students(self.students)
        return new_student, f"\n\t\033[33mStudent {name} registered successfully.\033[0m"

    def change_password(self, student, new_password, confirm_password):
        Database.load_students()
        if not re.fullmatch(PASSWORD_PATTERN, new_password):
            return "\n\t\t\033[31mInvalid password format.\033[0m"
        if new_password != confirm_password:
            return "\n\t\t\033[31mPasswords do not match.\033[0m"
        student.password = new_password
        Database.save_students(self.students)
        return "\n\t\t\033[32mPassword changed successfully.\033[0m"

    def get_all_students(self):
        Database.load_students()
        return self.students

    def save_students(self):
        Database.save_students(self.students)
