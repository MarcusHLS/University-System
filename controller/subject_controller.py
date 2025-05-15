import random
from model.subject import Subject
from model.database import Database

class SubjectController:
    def __init__(self):
        self.students = Database.load_data()

    def enrol_subject(self, student):
        if len(student.subjects) >= 4:
            return None

        existing_ids = set()
        for s in self.students:
            for subj in s.subjects:
                existing_ids.add(subj.id)

        while True:
            new_id = str(random.randint(1, 999)).zfill(3)
            if new_id not in existing_ids:
                break

        new_subject = Subject(id=new_id)
        student.enrol_subject(new_subject)

        for i, s in enumerate(self.students):
            if s.id == student.id:
                self.students[i] = student
                break

        Database.save_data(self.students)
        return new_subject



    def remove_subject(self, student, subject_id):
        subject_id = str(subject_id).zfill(3)  

        found = False
        for subj in student.subjects:
            if subj.id == subject_id:
                found = True
                break

        if found:
            student.remove_subject(subject_id)
            for i, s in enumerate(self.students):
                if s.id == student.id:
                    self.students[i] = student
                    break
            Database.save_data(self.students)
            return True
        else:
            return False



    def show_subjects(self, student):
        return student.subjects