from model.database import Database
from model.student import Student

class AdminController:
    def __init__(self):
        self.students = Database.load_students()

    def clear_database(self, confirm=False):
        if confirm:
            self.students.clear()
            Student.used_ids.clear()
            Database.clear_database()
            return "\033[32mAll student data cleared.\033[0m"
        else:
            return "\033[33mOperation cancelled.\033[0m"

    def show_all_students(self):
        self.students = Database.load_students()
        if not self.students:
            return "\033[33m< Nothing to Display >\033[0m"
        result = ["\033[33mStudent List:\033[0m"]
        for student in self.students:
            result.append(f"\t{student.name:<15} :: {student.id} --> Email: {student.email}")
        return "\n".join(result)

    def group_students_by_grade(self):
        self.students = Database.load_students()
        if not self.students:
            return "\033[33mNo students to group.\033[0m"

        grade_groups = {'HD': [], 'D': [], 'C': [], 'P': [], 'Z': []}

        for student in self.students:
            student.update_mark()
            student.update_grade()
            info = f"{student.name:<15} :: {student.id} --> GRADE: {student.grade} - MARK: {student.mark:.2f}"
            grade_groups[student.grade].append(info)

        output = ["\033[33mGrade Grouping:\033[0m"]
        for grade in ['HD', 'D', 'C', 'P', 'Z']:
            if grade_groups[grade]:
                group_str = " | ".join(grade_groups[grade])
                output.append(f"\033[36m{grade}\033[0m: [{group_str}]")
        return "\n".join(output)

    def partition_students(self):
        self.students = Database.load_students()
        if not self.students:
            return "\033[33mNo students to partition.\033[0m"

        pass_list, fail_list = [], []
        for student in self.students:
            student.update_mark()
            student.update_grade()
            info = f"{student.name:<15} :: {student.id} --> GRADE: {student.grade} - MARK: {student.mark:.2f}"
            if student.grade == 'Z':
                fail_list.append(info)
            else:
                pass_list.append(info)

        output = ["\033[33mPartitioning Students:\033[0m"]
        output.append(f"\033[36mPASS\033[0m: [{' ; '.join(pass_list)}]")
        output.append(f"\033[36mFAIL\033[0m: [{' ; '.join(fail_list)}]")
        return "\n".join(output)

    def remove_student_by_id(self, student_id):
        self.students = Database.load_students()
        student_to_remove = None
        for student in self.students:
            if student.id == student_id:
                student_to_remove = student
                break

        if student_to_remove:
            self.students.remove(student_to_remove)
            if int(student_id) in Student.used_ids:
                Student.used_ids.remove(int(student_id))
            Database.save_students(self.students)
            return f"\033[32mStudent {student_id} removed successfully.\033[0m"
        else:
            return f"\033[31mStudent ID {student_id} not found.\033[0m"

    def save_students(self):
        Database.save_students(self.students)

    def get_all_students(self):
        return self.students
