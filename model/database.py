import pickle
import os

# === Database Class ===
class Database:
    FILE_NAME = "students.data"

    @staticmethod
    def ensure_file_exists():
        if not os.path.exists(Database.FILE_NAME):
            with open(Database.FILE_NAME, 'wb') as f:
                pickle.dump([], f)

    @staticmethod
    def save_students(student_list):
        with open(Database.FILE_NAME, 'wb') as f:
            pickle.dump(student_list, f)
        # print("\t\033[32mDatabase updated.\033[0m")

    @staticmethod
    def load_students():
        Database.ensure_file_exists()
        with open(Database.FILE_NAME, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def clear_database():
        with open(Database.FILE_NAME, 'wb') as f:
            pickle.dump([], f)