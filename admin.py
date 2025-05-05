from student import Student
from database import Database

# === Admin Class ===
class Admin:
    def clear_database(self, university):
        confirm = input("\t\033[31mAre you sure you want to clear all student data? (y/n):\033[0m ").lower()
        if confirm == 'y':
            university.student.clear()
            Student.used_ids.clear()
            Database.clear_database()
        else:
            print("\t\033[31mOperation cancelled.\033[0m")

    def group_students_by_grade(self, university):
        print("\n\t\033[33mGrade Grouping\033[0m")
        if not university.student:
            print("\tNo students to group.")
            return

        grade_groups = {'HD': [], 'D': [], 'C': [], 'P': [], 'Z': []}

        for student in university.student:
            student.update_mark()
            student.update_grade()
            info = f"{student.name:<15} :: {student.id} --> GRADE: {student.grade:3} - MARK: {student.mark:.2f}"
            grade_groups[student.grade].append(info)

        for grade in ['HD', 'D', 'C', 'P', 'Z']:
            if grade_groups[grade]:
                print(f"\t{grade:3}  --> [", end="")
                print(" | ".join(grade_groups[grade]), end="]\n")

    def partition_students(self, university):
        print("\n\t\033[33mPartitioning Students\033[0m")
        if not university.student:
            print("\tNo students to partition.")
            return

        pass_list, fail_list = [], []

        for student in university.student:
            student.update_mark()
            student.update_grade()
            info = f"{student.name:<15} :: {student.id} --> GRADE: {student.grade:3} - MARK: {student.mark:.2f}"
            (fail_list if student.grade == 'Z' else pass_list).append(info)

        print(f"\tFAIL --> [{', '.join(fail_list)}]")
        print(f"\tPASS --> [{', '.join(pass_list)}]")

    def remove_student_by_id(self, university):
        if not university.student:
            print("\tNo students in database")
            return
        student_id = input("\tRemove by ID: ")
        for student in university.student:
            if student.id == student_id:
                university.student.remove(student)
                Student.used_ids.remove(int(student_id))
                Database.save_students(university.student)
                print(f"\t\033[33mRemoved Student {student_id} Account\033[0m")
                return
        print(f"\t\033[31mStudent {student_id} does not exist\033[0m")

    def show_all_students(self, university):
        print("\t\033[33mStudent List\033[0m")
        if not university.student:
            print("\t\t< Nothing to Display >")
            return
        for student in university.student:
            print(f"\t{student.name:<15} :: {student.id} --> Email: {student.email}")