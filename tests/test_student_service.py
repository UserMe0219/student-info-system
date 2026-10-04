import json
import tempfile
import unittest
from pathlib import Path

from src.services.student_service import StudentService


class StudentServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_file = Path(self.temp_dir.name) / "students.json"
        self.service = StudentService(str(self.db_file))
        self.student = {
            "student_id": "S001",
            "name": "Alex",
            "course": "Computer Science",
            "year_level": "1",
        }
        self.service.add_student(self.student)

    def test_update_student_changes_provided_fields_only(self):
        result = self.service.update_student(
            "S001", {"course": "Information Technology"}
        )

        self.assertEqual(result, (True, "Student updated successfully."))
        self.assertEqual(
            self.service.get_all_students(),
            [
                {
                    **self.student,
                    "course": "Information Technology",
                }
            ],
        )

    def test_update_student_missing_id_does_not_change_data(self):
        result = self.service.update_student("missing", {"name": "Sam"})

        self.assertEqual(result, (False, "Student ID not found."))
        self.assertEqual(self.service.get_all_students(), [self.student])

    def test_update_persists_valid_json(self):
        self.service.update_student("S001", {"name": "Sam"})

        with self.db_file.open("r", encoding="utf-8") as file:
            self.assertEqual(json.load(file)[0]["name"], "Sam")


if __name__ == "__main__":
    unittest.main()
