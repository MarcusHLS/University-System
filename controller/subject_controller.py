from model.student import Subject
from model.database import Database

class SubjectController:
    def __init__(self, students):
        self.students = students  

    def enrol_subject(self, student):
        students = Database.load_students()
        for s in students:
            if s.email == student.email:
                if len(s.subject) >= 4:
                    return f"\n\t\t\033[31mStudent {s.name} is already enrolled in 4 subjects.\033[0m"
                new_subject = Subject()
                s.subject.append(new_subject)
                s.update_mark()
                s.update_grade()
                Database.save_students(students)
                return f"\n\t\t\033[33mEnrolled in Subject ID {new_subject.id}. Total subjects: {len(s.subject)}\033[0m"
        return "\n\t\t\033[31mStudent not found in database.\033[0m"


    def remove_subject(self, student, subject_id):
        students = Database.load_students()
        for s in students:
            if s.email == student.email:
                found = next((sub for sub in s.subject if sub.id == subject_id), None)
                if not found:
                    return f"\n\t\t\033[31mSubject ID {subject_id} not found for student {s.name}.\033[0m"
                s.subject.remove(found)
                s.update_mark()
                s.update_grade()
                Database.save_students(students)
                return f"\n\t\t\033[32mSubject ID {subject_id} removed. Remaining subjects: {len(s.subject)}\033[0m"
        return f"\n\t\t\033[31mStudent {student.email} not found in database.\033[0m"

    def get_subjects(self, student):
        students = Database.load_students()
        if not student.subject:
            return "\t\t < No subjects enrolled. >"

        result = ["\t\tSubject List:"]
        for sub in student.subject:
            # Align ID to 3 characters, mark to 3 width, grade to 3 width
            result.append(f"\t\t[ Subject ID::{sub.id:>3} -- Mark: {sub.mark:>3} -- Grade: {sub.grade:<3} ]")
        return "\n".join(result)

    def get_subject_count(self, student):
        return len(student.subject)
