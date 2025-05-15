# University Management System

A **MVC-based** university student management system supporting both **Command Line Interface (CLI)** and **Graphical User Interface (GUI)**. It provides features for student login, course enrollment, course removal, subject viewing, and administrator operations.

---

## ✨ Features

✅ Student login using validated credentials  
✅ Maximum of 4 enrolled subjects per student  
✅ Automatic generation of subject marks and grades (HD/D/C/P/F)  
✅ Students can view or remove enrolled subjects  
✅ Administrator functions:
- Clear the student database
- Group students by grade
- Partition students by pass/fail
- Remove student by ID
- Display all students

✅ **Consistent CLI formatting with indentations and colored output (via `colorama`)**  
✅ **GUI interface (built with Tkinter)**

---

## 🏗️ Project Structure

```bash
├── app.py                 # Main entry point
├── controllers/
│   ├── admin_controller.py
│   ├── student_controller.py
│   └── subject_controller.py
├── models/
│   ├── student.py
│   ├── database.py
│   └── subject.py
├── views/
│   ├── cli_view.py
│   └── gui_view.py
├── students.data          # Student data file (pickle format)
```

------

## 🚀 How to Run

### 1️⃣ **Run CLI Interface**

```bash
python app.py
```

When prompted, enter `1` to launch the command-line version.

👉 CLI uses **clear indentation and colored output using `colorama`** for improved readability.

------

### 2️⃣ **Run GUI Interface**

```bash
python app.py
```

When prompted, enter `2` to launch the graphical interface.

Alternatively, run directly:

```bash
python views/gui_view.py
```

------

## ⚙️ Requirements

✅ Python 3.7+  
✅ Tkinter (included in Python standard library)  
✅ `colorama` for CLI color support

Install dependencies (if needed):

```bash
pip install colorama
```

For Linux, if Tkinter is missing:

```bash
sudo apt-get install python3-tk
```

(Windows and macOS usually have it pre-installed)

------

## 📚 Data Storage

Student data is saved in `students.data` (pickle format).  
Deleting or clearing this file will result in loss of stored data.

The admin's "clear database" option will also reset this file.

------

## 📝 Author

Developed by Group 4

------

## 🧩 Notes

✅ Supports both CLI and GUI modes for different user types  
✅ CLI formatting consistent with specification (indentation, wording, layout)  
✅ CLI uses `colorama` for colored terminal output (compatible with most modern terminals)

⚠️ GUI is accessible only for pre-registered students. Registration must be completed via CLI.
