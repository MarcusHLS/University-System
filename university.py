from database import Database
from admin import Admin
from student import Student
import re

# === Constants ===
EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

# === University Class ===
class University:
    def __init__(self):
        self.student = Database.load_students()
        self.admin = Admin()

    def system_menu(self):
        while True:
            choice = input("\033[36mUniversity System: (A)dmin, (S)tudent, or X:\033[0m ").upper()
            if choice == 'A':
                self.admin_system()
            elif choice == 'S':
                self.student_system()
            elif choice == 'X':
                print("\033[33mThank You")
                break
            else:
                print("\033[31mInvalid input. Please try again\033[0m")

    def admin_system(self):
        while True:
            choice = input("\t\033[36mAdmin System (c/g/p/r/s/x):\033[0m ").lower()
            if choice == 'c':
                self.admin.clear_database(self)
            elif choice == 'g':
                self.admin.group_students_by_grade(self)
            elif choice == 'p':
                self.admin.partition_students(self)
            elif choice == 'r':
                self.admin.remove_student_by_id(self)
            elif choice == 's':
                self.admin.show_all_students(self)
            elif choice == 'x':
                print("\t\033[33mExit Admin System\033[0m")
                break
            else:
                print("\t\033[31mInvalid input. Please try again\033[0m")

    def student_system(self):
        while True:
            choice = input("\t\033[36mStudent System (l/r/x):\033[0m ").lower()
            if choice == 'l':
                student = self.student_login()
                if not student:
                    print("\t\033[31mLogin failed. Student not found or password incorrect.\033[0m")
                    continue
                self.student_course_menu(student)
            elif choice == 'r':
                self.student_register()
            elif choice == 'x':
                print("\t\033[33mExit Student System\033[0m")
                break
            else:
                print("\t\033[31mInvalid input. Please try again\033[0m")

    def student_login(self):
        print("\t\033[33mStudent Sign In\033[0m")
        email = input("\tEmail: ")
        password = input("\tPassword: ")
        while not (re.fullmatch(EMAIL_PATTERN, email) and re.fullmatch(PASSWORD_PATTERN, password)):
            print("\t\033[31mIncorrect email or password format\033[0m")
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()
        print("\t\033[33mEmail and password formats acceptable\033[0m")
        for student in self.student:
            if student.email == email and student.password == password:
                print(f"\t\033[36mWelcome back, {student.name}!\033[0m")
                return student
        return None

    def student_register(self):
        print("\t\033[33mStudent Sign Up\033[0m")
        email = input("\tEmail: ").strip()
        password = input("\tPassword: ").strip()
        while not (re.fullmatch(EMAIL_PATTERN, email) and re.fullmatch(PASSWORD_PATTERN, password)):
            print("\t\033[31mIncorrect email or password format\033[0m")
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()
        print("\t\033[33mEmail and password formats acceptable\033[0m")
        for student in self.student:
            if student.email == email:
                print(f"\t\033[31mStudent {student.name} already exists\033[0m")
                return
        name = input("\tName: ")
        if not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)*", name):
            print("\t\033[31mInvalid name. Only letters and a single space allowed.\033[0m")
            return
        print(f"\t\033[33mEnrolling Student {name}\033[0m")
        self.student.append(Student(name, email, password))
        Database.save_students(self.student)

    def student_course_menu(self, student):
        while True:
            choice = input("\t\t\033[36mStudent Course Menu (c/e/r/s/x):\033[0m ").lower()
            if choice == 'c':
                student.change_password(self.student)
            elif choice == 'e':
                student.enrol_subject(self.student)
            elif choice == 'r':
                student.remove_subject(self.student)
            elif choice == 's':
                student.show_subject()
            elif choice == 'x':
                print("\t\t\033[33mExit Student Course Menu\033[0m")
                break
            else:
                print("\t\t\033[31mInvalid input. Please try again\033[0m")