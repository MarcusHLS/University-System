import random

class Subject:
    used_ids = set()

    def __init__(self, mark=None):
        self.id = self.generate_unique_id()
        self.mark = mark if mark is not None else random.randint(25, 100)
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

    def update_mark(self, new_mark):
        self.mark = new_mark
        self.grade = self.calculate_grade()
