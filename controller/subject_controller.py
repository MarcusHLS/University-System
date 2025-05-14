from model.student import Subject
from model.database import Database

class SubjectController:
    def __init__(self, students):
        self.students = students  

    def enrol_subject(self, student):
        if len(student.subject) >= 4:
            return f"\n\t\t\033[31mStudent {student.name} is already enrolled in 4 subjects.\033[0m"
        new_subject = Subject()
        student.subject.append(new_subject)
        student.update_mark()
        student.update_grade()
        Database.save_students(self.students)
        return f"\n\t\t\033[33mEnrolled in Subject ID {new_subject.id}. Total subjects: {len(student.subject)}\033[0m"

    def remove_subject(self, student, subject_id):
        found = next((sub for sub in student.subject if sub.id == subject_id), None)
        if not found:
            return f"\n\t\t\033[31mSubject ID {subject_id} not found for student {student.name}.\033[0m"
        student.subject.remove(found)
        student.update_mark()
        student.update_grade()
        Database.save_students(self.students)
        return f"\n\t\t\033[32mSubject ID {subject_id} removed. Remaining subjects: {len(student.subject)}\033[0m"

    def get_subjects(self, student):
        if not student.subject:
            return "\t\t < No subjects enrolled. >"

        result = ["\t\tSubject List:"]
        for sub in student.subject:
            # Align ID to 3 characters, mark to 3 width, grade to 3 width
            result.append(f"\t\t  [ Subject ID::{sub.id:>3} -- Mark: {sub.mark:>3} -- Grade: {sub.grade:<3} ]")
        return "\n".join(result)

    def get_subject_detail(self, student, subject_id):
        found = next((sub for sub in student.subject if sub.id == subject_id), None)
        if not found:
            return f"\n\t\t\033[31mSubject ID {subject_id} not found.\033[0m"
        return f"\n\t\t\033[36mSubject Detail:\033[0m\n  ID: {found.id}\n  Mark: {found.mark}\n  Grade: {found.grade}"

    def get_subject_count(self, student):
        return len(student.subject)
