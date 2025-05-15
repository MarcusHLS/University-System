import random
from model.subject import Subject

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(0, 999999)).zfill(6)  
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def enrol_subject(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)
            return True
        return False

    def remove_subject(self, subject_id):
        subject_id = str(subject_id).zfill(3)
        self.subjects = [s for s in self.subjects if s.id != subject_id]


    def calculate_average(self):
        if not hasattr(self, "subjects") or not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def get_grade_group(self):
        avg = self.calculate_average()
        if avg >= 85:
            return "HD"
        elif avg >= 75:
            return "D"
        elif avg >= 65:
            return "C"
        elif avg >= 50:
            return "P"
        else:
            return "F"
