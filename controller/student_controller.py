from model.student import Student
from model.database import Database
import re

EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

class StudentController:
    def __init__(self):
        self.students = Database.load_students()

    def login(self, email, password):
        if not (re.fullmatch(EMAIL_PATTERN, email) and re.fullmatch(PASSWORD_PATTERN, password)):
            return None, "\033[31mInvalid email or password format.\033[0m"
        for student in self.students:
            if student.email == email and student.password == password:
                return student, f"\033[36mWelcome back, {student.name}!\033[0m"
        return None, "\033[31mStudent not found or incorrect password.\033[0m"

    def register(self, name, email, password):
        if not re.fullmatch(EMAIL_PATTERN, email):
            return None, "\033[31mInvalid email format.\033[0m"
        if not re.fullmatch(PASSWORD_PATTERN, password):
            return None, "\033[31mInvalid password format.\033[0m"
        if any(s.email == email for s in self.students):
            return None, f"\033[31mStudent with email {email} already exists.\033[0m"

        new_student = Student(name, email, password)
        self.students.append(new_student)
        Database.save_students(self.students)
        return new_student, f"\033[33mStudent {name} registered successfully.\033[0m"

    def change_password(self, student, new_password, confirm_password):
        if not re.fullmatch(PASSWORD_PATTERN, new_password):
            return "\033[31mInvalid password format.\033[0m"
        if new_password != confirm_password:
            return "\033[31mPasswords do not match.\033[0m"
        student.password = new_password
        Database.save_students(self.students)
        return "\033[32mPassword changed successfully.\033[0m"

    def enrol_subject(self, student):
        if len(student.subject) >= 4:
            return f"\033[31mStudent {student.name} is already enrolled in 4 subjects.\033[0m"
        student.enrol_subject(self.students)
        return f"\033[33mStudent {student.name} enrolled in new subject. Total subjects: {len(student.subject)}\033[0m"

    def remove_subject(self, student, subject_id):
        found = next((sub for sub in student.subject if sub.id == subject_id), None)
        if not found:
            return f"\033[31mSubject ID {subject_id} not found for student {student.name}.\033[0m"
        student.subject.remove(found)
        student.update_mark()
        student.update_grade()
        Database.save_students(self.students)
        return f"\033[32mSubject ID {subject_id} removed. Remaining subjects: {len(student.subject)}\033[0m"

    def show_subjects(self, student):
        if not student.subject:
            return "\033[33mNo subjects enrolled.\033[0m"
        result = ["\033[36mSubject List:\033[0m"]
        for sub in student.subject:
            result.append(f"  Subject ID: {sub.id}, Mark: {sub.mark}, Grade: {sub.grade}")
        return "\n".join(result)

    def get_all_students(self):
        return self.students

    def save_students(self):
        Database.save_students(self.students)
