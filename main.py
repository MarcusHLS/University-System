import threading
import tkinter as tk
from guiapp import GUIUniApp  
from university import University 

# Start the CLI interface in a thread
def run_cli():
    university = University()
    university.system_menu()

# Start the GUI interface
def run_gui():
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()

if __name__ == "__main__":
    cli_thread = threading.Thread(target=run_cli)
    cli_thread.start()

    run_gui()  # run GUI in the main thread