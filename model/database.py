import os
import pickle

class Database:
    FILE_NAME = "students.data"

    @staticmethod
    def load_data():
        if not os.path.exists(Database.FILE_NAME):
            return []
        with open(Database.FILE_NAME, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def save_data(data):
        with open(Database.FILE_NAME, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def clear_data():
        with open(Database.FILE_NAME, "wb") as f:
            pickle.dump([], f)
