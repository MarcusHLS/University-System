class CLIView:
    def __init__(self, student_controller, admin_controller, subject_controller):
        self.student_controller = student_controller
        self.admin_controller = admin_controller
        self.subject_controller = subject_controller

    def main_menu(self):
        while True:
            choice = input("\n\033[36mUniversity System: (A)dmin, (S)tudent, (X) Exit:\033[0m ").upper()
            if choice == 'A':
                self.admin_menu()
            elif choice == 'S':
                self.student_menu()
            elif choice == 'X':
                print("\033[33mThank you for using the system.\033[0m")
                break
            else:
                print("\033[31mInvalid input. Please try again.\033[0m")

    def admin_menu(self):
        while True:
            choice = input("\n\033[36mAdmin Menu: (C)lear DB, (G)roup Grades, (P)artition, (R)emove Student, (S)how All, (X) Exit:\033[0m ").upper()
            if choice == 'C':
                confirm = input("\033[33mAre you sure to clear database? (Y/N):\033[0m ").upper() == 'Y'
                message = self.admin_controller.clear_database(confirm)
                print(message)
            elif choice == 'G':
                message = self.admin_controller.group_students_by_grade()
                print(message)
            elif choice == 'P':
                message = self.admin_controller.partition_students()
                print(message)
            elif choice == 'R':
                student_id = input("\033[33mEnter Student ID to remove:\033[0m ")
                message = self.admin_controller.remove_student_by_id(student_id)
                print(message)
            elif choice == 'S':
                message = self.admin_controller.show_all_students()
                print(message)
            elif choice == 'X':
                print("\033[33mExit Admin Menu\033[0m")
                break
            else:
                print("\033[31mInvalid input.\033[0m")

    def student_menu(self):
        while True:
            choice = input("\n\033[36mStudent Menu: (L)ogin, (R)egister, (X) Exit:\033[0m ").upper()
            if choice == 'L':
                email = input("\033[33mEmail:\033[0m ")
                password = input("\033[33mPassword:\033[0m ")
                student, message = self.student_controller.login(email, password)
                print(message)
                if student:
                    self.student_course_menu(student)
            elif choice == 'R':
                name = input("\033[33mName:\033[0m ")
                email = input("\033[33mEmail:\033[0m ")
                password = input("\033[33mPassword:\033[0m ")
                student, message = self.student_controller.register(name, email, password)
                print(message)
            elif choice == 'X':
                print("\033[33mExit Student Menu\033[0m")
                break
            else:
                print("\033[31mInvalid input.\033[0m")

    def student_course_menu(self, student):
        while True:
            choice = input("\n\033[36mStudent Course Menu: (E)nrol, (R)emove, (S)how Subjects, (P)assword Change, (X) Exit:\033[0m ").upper()
            if choice == 'E':
                message = self.subject_controller.enrol_subject(student)
                print(message)
            elif choice == 'R':
                subject_id = input("\033[33mSubject ID to remove:\033[0m ")
                message = self.subject_controller.remove_subject(student, subject_id)
                print(message)
            elif choice == 'S':
                message = self.subject_controller.get_subjects(student)
                print(message)
            elif choice == 'P':
                new_password = input("\033[33mNew password:\033[0m ")
                confirm_password = input("\033[33mConfirm password:\033[0m ")
                message = self.student_controller.change_password(student, new_password, confirm_password)
                print(message)
            elif choice == 'X':
                print("\033[33mExit Student Course Menu\033[0m")
                break
            else:
                print("\033[31mInvalid input.\033[0m")
