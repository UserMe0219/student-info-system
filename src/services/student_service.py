import json
import os


class StudentService:
    def __init__(self, db_file):
        self.db_file = db_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        directory = os.path.dirname(self.db_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w", encoding="utf-8") as file:
                json.dump([], file)

    def load_students(self):
        with open(self.db_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_students(self, students):
        with open(self.db_file, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)

    def add_student(self, student_dict):
        students = self.load_students()
        if any(
            student["student_id"] == student_dict["student_id"]
            for student in students
        ):
            return False, "Student ID already exists."

        students.append(student_dict)
        self.save_students(students)
        return True, "Student added successfully."

    def get_all_students(self):
        return self.load_students()

    def update_student(self, student_id, updates):
        students = self.load_students()
        for student in students:
            if student["student_id"] == student_id:
                for field in ("name", "course", "year_level"):
                    if field in updates:
                        student[field] = updates[field]
                self.save_students(students)
                return True, "Student updated successfully."

        return False, "Student ID not found."

    def delete_student(self, student_id):
        students = self.load_students()
        remaining_students = [
            student
            for student in students
            if student["student_id"] != student_id
        ]

        if len(remaining_students) == len(students):
            return False, "Student ID not found."

        self.save_students(remaining_students)
        return True, "Student deleted successfully."
