# App.py
from view.CLI import main_menu
from view.GUI import GUIUniApp

def start_cli():
    main_menu()

def start_gui():
    app = GUIUniApp()
    app.run()

if __name__ == "__main__":
    print("Start Application Mode:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        start_cli()
    elif choice == "2":
        start_gui()
    else:
        print("Invalid choice. Exiting.")
