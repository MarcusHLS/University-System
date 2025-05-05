from model.student import Subject
from model.database import Database

class SubjectController:
    def __init__(self, students):
        self.students = students  

    def enrol_subject(self, student):
        if len(student.subject) >= 4:
            return f"\033[31mStudent {student.name} is already enrolled in 4 subjects.\033[0m"
        new_subject = Subject()
        student.subject.append(new_subject)
        student.update_mark()
        student.update_grade()
        Database.save_students(self.students)
        return f"\033[33mEnrolled in Subject ID {new_subject.id}. Total subjects: {len(student.subject)}\033[0m"

    def remove_subject(self, student, subject_id):
        found = next((sub for sub in student.subject if sub.id == subject_id), None)
        if not found:
            return f"\033[31mSubject ID {subject_id} not found for student {student.name}.\033[0m"
        student.subject.remove(found)
        student.update_mark()
        student.update_grade()
        Database.save_students(self.students)
        return f"\033[32mSubject ID {subject_id} removed. Remaining subjects: {len(student.subject)}\033[0m"

    def get_subjects(self, student):
        if not student.subject:
            return "\033[33mNo subjects enrolled.\033[0m"
        result = ["\033[36mSubject List:\033[0m"]
        for sub in student.subject:
            result.append(f"  Subject ID: {sub.id}, Mark: {sub.mark}, Grade: {sub.grade}")
        return "\n".join(result)

    def get_subject_detail(self, student, subject_id):
        found = next((sub for sub in student.subject if sub.id == subject_id), None)
        if not found:
            return f"\033[31mSubject ID {subject_id} not found.\033[0m"
        return f"\033[36mSubject Detail:\033[0m\n  ID: {found.id}\n  Mark: {found.mark}\n  Grade: {found.grade}"

    def get_subject_count(self, student):
        return len(student.subject)
