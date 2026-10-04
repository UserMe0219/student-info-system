class Student:
    def __init__(self, student_id, name, course, year_level):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.year_level = year_level

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "course": self.course,
            "year_level": self.year_level,
        }

    @staticmethod
    def from_dict(data):
        return Student(
            student_id=data["student_id"],
            name=data["name"],
            course=data["course"],
            year_level=data["year_level"],
        )
