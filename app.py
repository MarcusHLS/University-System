import threading
import tkinter as tk
from view.CLI import main_menu
from view.GUI import GUIUniApp  

def run_cli():
    main_menu()

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
