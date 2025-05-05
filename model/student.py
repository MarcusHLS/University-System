import random
import re

EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

class Subject:
    used_ids = set()

    def __init__(self):
        self.id = self.generate_unique_id()
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def generate_unique_id(self):
        while True:
            id_num = random.randint(1, 999)
            if id_num not in Subject.used_ids:
                Subject.used_ids.add(id_num)
                return f'{id_num:03d}'

    def calculate_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'Z'

class Student:
    used_ids = set()

    def __init__(self, name, email, password):
        self.id = self.generate_unique_id()
        self.name = name
        self.email = email
        self.password = password
        self.subject = []
        self.mark = 0
        self.grade = 'Z'
        self.update_mark()
        self.update_grade()

    def generate_unique_id(self):
        while True:
            id_num = random.randint(1, 999999)
            if id_num not in Student.used_ids:
                Student.used_ids.add(id_num)
                return f'{id_num:06d}'

    def add_subject(self, subject):
        """Adds a subject instance to the student."""
        if len(self.subject) >= 4:
            raise ValueError("Cannot enrol in more than 4 subjects.")
        self.subject.append(subject)
        self.update_mark()
        self.update_grade()

    def remove_subject_by_id(self, subject_id):
        """Removes subject by ID."""
        subject_to_remove = next((s for s in self.subject if s.id == subject_id), None)
        if not subject_to_remove:
            raise ValueError(f"Subject ID {subject_id} not found.")
        self.subject.remove(subject_to_remove)
        self.update_mark()
        self.update_grade()

    def change_password(self, new_password):
        """Changes the student's password."""
        if not re.fullmatch(PASSWORD_PATTERN, new_password):
            raise ValueError("Invalid password format.")
        self.password = new_password

    def calculate_mark(self):
        if not self.subject:
            return 0
        return sum(s.mark for s in self.subject) / len(self.subject)

    def update_mark(self):
        self.mark = self.calculate_mark()

    def update_grade(self):
        if self.mark >= 85:
            self.grade = 'HD'
        elif self.mark >= 75:
            self.grade = 'D'
        elif self.mark >= 65:
            self.grade = 'C'
        elif self.mark >= 50:
            self.grade = 'P'
        else:
            self.grade = 'Z'
