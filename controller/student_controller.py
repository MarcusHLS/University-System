from model.database import Database
from model.student import Student
from model.subject import Subject

class StudentController:
    def __init__(self):
        self.students = Database.load_data()

    def register(self, name, email, password):
        if not self.validate_credentials(email, password):
            return "invalid_format"
        if any(s.email == email for s in self.students):
            return "exists"
        if any(s.name == name for s in self.students):
            return "exists"
        new_student = Student(name, email, password)
        self.students.append(new_student)
        Database.save_data(self.students)
        return "registered"

    def login(self, email, password):
        for s in self.students:
            if s.email == email and s.password == password:
                return s
        return None

    def change_password(self, student, new_password, confirm_password):
        if new_password != confirm_password:
            return "mismatch"
        if not self._is_valid_password(new_password):
            return "invalid_format"

        for i, s in enumerate(self.students):
            if s.id == student.id:
                self.students[i].password = new_password
                student.password = new_password

                Database.save_data(self.students)
                return "changed"
        return "not_found"



    def validate_credentials(self, email, password):
        return self._is_valid_email(email) and self._is_valid_password(password)

    def _is_valid_email(self, email):
        domain = "@university.com"
        if not email.endswith(domain):
            return False
        local_part = email[:-len(domain)]
        if '.' not in local_part:
            return False
        parts = local_part.split('.')
        if len(parts) != 2:
            return False
        firstname, lastname = parts
        return firstname.isalpha() and lastname.isalpha() and firstname and lastname

    def _is_valid_password(self, password):
        if len(password) < 8:
            return False
        if not password[0].isupper():
            return False

        letters = [c for c in password if c.isalpha()]
        digits = [c for c in password if c.isdigit()]

        if len(letters) <= 5 or len(digits) < 3:
            return False

        # Ensure digits come after letters
        first_digit_index = next((i for i, c in enumerate(password) if c.isdigit()), len(password))
        return all(c.isdigit() for c in password[first_digit_index:])

    def email_exists(self, email):
        for s in self.students:
            if s.email == email:
                return s.name
        return False

    def student_exists(self, name):
        return any(s.name == name for s in self.students)
