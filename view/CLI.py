from controller.student_controller import StudentController
from controller.subject_controller import SubjectController
from controller.admin_controller import AdminController
from colorama import init, Fore, Style

init()  
FIRST_INDENTATION = "   "
SEC_INDENTATION = "      "
Thr_INDENTATION = "         "

def main_menu():
    while True:
        print(Fore.CYAN + "University System: (A)dmin, (S)tudent, or X : " + Style.RESET_ALL, end="")
        choice = input().strip().upper()
        if choice == "A":
            admin_menu()
        elif choice == "S":
            student_menu()
        elif choice == "X":
            print(Fore.YELLOW + "Thank You" + Style.RESET_ALL)
            break

def admin_menu():
    admin = AdminController()
    while True:
        print(Fore.CYAN + FIRST_INDENTATION + "Admin System (c/g/p/r/s/x): " + Style.RESET_ALL, end="")
        choice = input().strip().lower()

        if choice == "c":
            print(Fore.YELLOW + FIRST_INDENTATION + "Clearing students database" + Style.RESET_ALL)
            confirm = input(Fore.RED + FIRST_INDENTATION + "Are you sure you want to clear the database (Y)ES/(N)O: " + Style.RESET_ALL).strip().upper()
            if confirm == "Y":
                admin.clear_database()
                print(Fore.YELLOW + FIRST_INDENTATION + "Students data cleared" + Style.RESET_ALL)
            elif confirm == "N":
                continue
            else:
                print(Fore.RED + FIRST_INDENTATION + "Invalid command. Please try again!" + Style.RESET_ALL)

        elif choice == "g":
            print(Fore.YELLOW + FIRST_INDENTATION + "Grade Grouping" + Style.RESET_ALL)
            groups = admin.group_students()
            if not any(groups.values()):
                print(SEC_INDENTATION + "< Nothing to Display >" + Style.RESET_ALL)
            else:
                for grade, students in groups.items():
                    if len(students)>0:
                        print( f"{FIRST_INDENTATION}{grade} -->" , end="")
                        if not students:
                            print("[]")
                        else:
                            print(" [" + ', '.join(
                                f"{s.name:<15} :: {s.id} --> GRADE:  {grade:<3} -- MARK: {s.calculate_average():.2f}" for s in students
                            ) + "]")
        elif choice == "p":
            print(Fore.YELLOW + FIRST_INDENTATION + "PASS/FAIL Partition" + Style.RESET_ALL)
            partition = admin.partition_students()
            for status, students in partition.items():
                if not students:
                    print(FIRST_INDENTATION+f"{status} --> []")
                else:
                    details = ', '.join(
                        f"{s.name} :: {s.id} --> GRADE:  {s.get_grade_group():<2} -- MARK: {s.calculate_average():.2f}"
                        for s in students
                    )
                    print(FIRST_INDENTATION+f"{status} --> [{details}]")

        elif choice == "r":
            print(Fore.CYAN + FIRST_INDENTATION + "Remove by ID: " + Style.RESET_ALL, end="")
            try:
                sid = str(input())
                success = admin.remove_student(sid)
                if success:
                    print(Fore.YELLOW + FIRST_INDENTATION + f"Removing Student {sid} Account" + Style.RESET_ALL)
                else:
                    print(Fore.RED + FIRST_INDENTATION + f"Student {sid} does not exist" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + FIRST_INDENTATION + "Invalid ID format" + Style.RESET_ALL)

        elif choice == "s":
            print(Fore.YELLOW + FIRST_INDENTATION + "Student List" + Style.RESET_ALL)
            students = admin.list_students()
            if not students:
                print(SEC_INDENTATION + "< Nothing to Display >" + Style.RESET_ALL)
            else:
                for s in students:
                    print(FIRST_INDENTATION + f"{s.name:<15} :: {s.id} --> Email: {s.email}")

        elif choice == "x":
            break

def student_menu():
    controller = StudentController()
    while True:
        print(Fore.CYAN + FIRST_INDENTATION + "Student System (l/r/x): " + Style.RESET_ALL, end="")
        choice = input().strip().lower()
        if choice == "r":
            print(Fore.GREEN + FIRST_INDENTATION + "Student Sign Up" + Style.RESET_ALL)

            email = ""
            while True:
                email = input(FIRST_INDENTATION + "Email: ")
                password = input(FIRST_INDENTATION + "Password: ")

                if not controller.validate_credentials(email, password):
                    print(Fore.RED + FIRST_INDENTATION + "Incorrect email or password format." + Style.RESET_ALL)
                    continue
                break

            print(Fore.YELLOW + FIRST_INDENTATION + "Email and password formats acceptable" + Style.RESET_ALL)
            student_exist = controller.email_exists(email)
            if student_exist != False:
                print(Fore.RED + FIRST_INDENTATION + f"Student {student_exist} already exists." + Style.RESET_ALL)
                continue
            name = input(FIRST_INDENTATION + "Name: ")
            if controller.student_exists(name):
                print(Fore.RED + FIRST_INDENTATION + f"Student {name} already exists." + Style.RESET_ALL)
                continue
            controller.register(name,email,password)
            print(Fore.YELLOW + FIRST_INDENTATION + f"Enrolling Student {name}" + Style.RESET_ALL)

        elif choice == "l":
            print(Fore.GREEN + FIRST_INDENTATION + "Student Sign In" + Style.RESET_ALL)
            email = ""

            while True:
                email = input(FIRST_INDENTATION + "Email: ")
                password = input(FIRST_INDENTATION + "Password: ")

                if not controller.validate_credentials(email, password):
                    print(Fore.RED + FIRST_INDENTATION + "Incorrect email or password format." + Style.RESET_ALL)
                    continue
                break

            print(Fore.YELLOW + FIRST_INDENTATION + "Email and password formats acceptable" + Style.RESET_ALL)
            student = controller.login(email, password)
            if student:
                subject_menu(student, controller)
            else:
                print(Fore.RED + FIRST_INDENTATION + "Student does not exist" + Style.RESET_ALL)
        elif choice == "x":
            break

def subject_menu(student, controller):
    subject_ctrl = SubjectController()
    print(f"{Fore.CYAN + SEC_INDENTATION}Welcome come back, {student.name}! {Style.RESET_ALL}")
    while True:
        print(Fore.CYAN + SEC_INDENTATION + "Student Course Menu (c/e/r/s/x): " + Style.RESET_ALL, end="")
        choice = input().strip().lower()
        if choice == "c":
            print(Fore.YELLOW + SEC_INDENTATION + "Updating Password" + Style.RESET_ALL)
            new_pw = input(SEC_INDENTATION + "New Password: ")
            confirm_pw = input(SEC_INDENTATION + "Confirm Password: ")
            result = controller.change_password(student, new_pw, confirm_pw)
            if result == "mismatch":
                print(Fore.RED + SEC_INDENTATION + "Password does not match – try again" + Style.RESET_ALL)
            print(Fore.GREEN + SEC_INDENTATION + "Your password has been changed successfully!")

        elif choice == "e":
            if len(student.subjects) < 4:
                subj = subject_ctrl.enrol_subject(student)
                print(Fore.YELLOW + SEC_INDENTATION + f"Enrolling in Subject-{subj.id}" + Style.RESET_ALL)
                print(Fore.YELLOW + SEC_INDENTATION + f"You are now enrolled in {len(student.subjects)} out of 4 subjects" + Style.RESET_ALL)
            else:
                print(Fore.RED + SEC_INDENTATION + "Students are allowed to enrol in 4 subjects only" + Style.RESET_ALL)

        elif choice == "r":
            sid = int(input(Fore.YELLOW + SEC_INDENTATION + "Remove Subject by ID: "))
            success = subject_ctrl.remove_subject(student, sid)
            if success:
                print(Fore.YELLOW + SEC_INDENTATION + f"Dropping Subject-{str(sid).zfill(3)}" + Style.RESET_ALL)
                print(Fore.YELLOW + SEC_INDENTATION + f"You are now enrolled in {len(student.subjects)} out of 4 subjects" + Style.RESET_ALL)
            else:
                print(Fore.RED + SEC_INDENTATION + f"Subject-{str(sid).zfill(3)} not found in your enrolled subjects." + Style.RESET_ALL)
                    
        elif choice == "s":
            if not student.subjects:
                print(Fore.YELLOW + SEC_INDENTATION + " < Nothing to display >" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + SEC_INDENTATION + f"Showing {len(student.subjects)} subjects" + Style.RESET_ALL)
                for subj in student.subjects:
                    print(SEC_INDENTATION + f"[ Subject::{subj.id.zfill(3)} -- Mark = {subj.mark:<3} -- Grade = {subj.grade:<2} ]")

        elif choice == "x":
            break
