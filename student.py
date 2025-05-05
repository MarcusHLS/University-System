import random
import sys
import re
import os
import pickle
from database import Database

# === Constants ===
EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

# === Subject Class ===
class Subject:
    used_ids = set()

    def __init__(self):
        self.id = self.generate_unique_id()
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def generate_unique_id(self):
        while True:
            id_num = random.randint(1, 999)
            if id_num not in Subject.used_ids:
                Subject.used_ids.add(id_num)
                return f'{id_num:03d}'

    def calculate_grade(self):
        if self.mark >= 85:
            return 'HD'
        elif self.mark >= 75:
            return 'D'
        elif self.mark >= 65:
            return 'C'
        elif self.mark >= 50:
            return 'P'
        else:
            return 'Z'

# === Student Class ===
class Student:
    used_ids = set()

    def __init__(self, name, email, password):
        self.id = self.generate_unique_id()
        self.name = name
        self.email = email
        self.password = password
        self.subject = []
        self.mark = self.calculate_mark()
        self.grade = 'Z'

    def generate_unique_id(self):
        while True:
            id_num = random.randint(1, 999999)
            if id_num not in Student.used_ids:
                Student.used_ids.add(id_num)
                return f'{id_num:06d}'

    def enrol_subject(self, student_list):
        if len(self.subject) >= 4:
            print('\t\t\033[31mStudent are allowed to enrol in 4 subjects only\033[0m')
            return
        new_subject = Subject()
        self.subject.append(new_subject)
        self.update_mark()
        self.update_grade()
        Database.save_students(student_list)
        print(f'\t\t\033[33mEnrolling in Subject-{new_subject.id}\033[0m')
        print(f'\t\t\033[33mYou are now enrolled in {len(self.subject)} out of 4 subjects\033[0m')

    def remove_subject(self, student_list):
        sub_id = input("\t\tRemove Subject by ID: ").strip()
        if not sub_id.isdigit():
            print(f"\t\t\033[31mInvalid Subject ID: Must be a number.\033[0m")
            return
        check = False
        for subject in self.subject:
            if subject.id == sub_id:
                self.subject.remove(subject)
                # Subject.used_ids.remove((subject.id))
                self.update_mark()
                self.update_grade()
                Database.save_students(student_list)
                check = True
                print(f"\t\t\033[33mDropping Subject-{subject.id}\033[0m")
                break
        if not check:
            print(f"\t\t\033[31mSubject is not exist\033[0m")
        else:
            print(f"\t\tYou are now enrolled in {len(self.subject)} out of 4 subjects")

    def show_subject(self):
        if not self.subject:
            print(f"\t\tYou are currently not enrolled in any subject")
            return
        for subject in self.subject:
            print(f"\t\t[ Subject::{subject.id} -- mark = {subject.mark} -- grade = {subject.grade}]")

    def change_password(self, student_list):
        new_password = input("\t\tNew password: ").strip()
        if not re.fullmatch(PASSWORD_PATTERN, new_password):
            print("\t\t\033[31mInvalid format. Start with uppercase, 5+ letters, end with 3+ digits.\033[0m")
            return
        confirm_password = input("\t\tConfirm password: ").strip()
        while new_password != confirm_password:
            print("\t\t\033[31mPasswords do not match - try again\033[0m")
            confirm_password = input("\t\tConfirm password: ").strip()
        self.password = new_password
        Database.save_students(student_list)
        print("\t\t\033[32mYour password has been changed.\033[0m")

    def calculate_mark(self):
        if not self.subject:
            return 0
        return sum(s.mark for s in self.subject) / len(self.subject)

    def update_mark(self):
        self.mark = self.calculate_mark()

    def update_grade(self):
        if self.mark >= 85:
            self.grade = 'HD'
        elif self.mark >= 75:
            self.grade = 'D'
        elif self.mark >= 65:
            self.grade = 'C'
        elif self.mark >= 50:
            self.grade = 'P'
        else:
            self.grade = 'Z'