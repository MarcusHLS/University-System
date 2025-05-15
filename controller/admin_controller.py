from model.database import Database

class AdminController:
    def __init__(self):
        self.students = Database.load_data()

    def clear_database(self):
        Database.clear_data()
        self.students = []

    def list_students(self):
        return self.students

    def group_students(self):
        groups = {"HD": [], "D": [], "C": [], "P": [], "F": []}
        for student in self.students:
            grade = student.get_grade_group()
            groups[grade].append(student)
        return groups

    def partition_students(self):
        partition = {"PASS": [], "FAIL": []}
        for student in self.students:
            if student.calculate_average() >= 50:
                partition["PASS"].append(student)
            else:
                partition["FAIL"].append(student)
        return partition

    def remove_student(self, student_id):
        student_id = str(student_id)  
        found = False
        updated_students = []

        for student in self.students:
            if student.id != student_id:
                updated_students.append(student)
            else:
                found = True  

        if found:
            self.students = updated_students
            Database.save_data(self.students)
            return True
        else:
            return False
