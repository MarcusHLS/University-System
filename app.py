import threading
import tkinter as tk
from controller.student_controller import StudentController
from controller.admin_controller import AdminController
from controller.subject_controller import SubjectController
from view.CLI import CLIView
from view.GUI import GUIUniApp  

def run_cli():
    student_controller = StudentController()
    admin_controller = AdminController()
    subject_controller = SubjectController(student_controller.students)

    cli_view = CLIView(student_controller, admin_controller, subject_controller)
    cli_view.main_menu()

def run_gui():
    root = tk.Tk()
    gui_app = GUIUniApp(root)  
    root.mainloop()

if __name__ == "__main__":
    mode = input("Choose interface: (C)LI or (G)UI? ").upper()

    if mode == "C":
        run_cli()
    elif mode == "G":
        run_gui()
    else:
        print("Invalid choice. Defaulting to CLI.")
        run_cli()
