import json
from pathlib import Path

from services.student_service import StudentService
from utils.logger import configure_logger


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config():
    config_path = PROJECT_ROOT / "config" / "config.json"
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    try:
        config = load_config()
        db_file = PROJECT_ROOT / config["db_file"]
        log_file = PROJECT_ROOT / config["log_file"]
        logger = configure_logger(str(log_file))
        service = StudentService(str(db_file))
    except (OSError, KeyError, json.JSONDecodeError) as error:
        print(f"Error initializing system: {error}")
        return

    logger.info("%s started", config.get("app_name", "Student Info System"))

    while True:
        print("\n--- Student Information System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        try:
            choice = input("Choose an option (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting... Goodbye!")
            break

        if choice == "1":
            student_data = {
                "student_id": input("Student ID: ").strip(),
                "name": input("Name: ").strip(),
                "course": input("Course: ").strip(),
                "year_level": input("Year Level: ").strip(),
            }
            success, message = service.add_student(student_data)
            print(message)
            logger.info("Add student result: %s", message)

        elif choice == "2":
            students = service.get_all_students()
            if not students:
                print("No students found.")
            else:
                print(
                    f"\n{'ID':<10} | {'Name':<20} | "
                    f"{'Course':<15} | {'Year':<5}"
                )
                print("-" * 55)
                for student in students:
                    print(
                        f"{student['student_id']:<10} | "
                        f"{student['name']:<20} | "
                        f"{student['course']:<15} | "
                        f"{student['year_level']:<5}"
                    )

        elif choice == "3":
            student_id = input("Enter Student ID to update: ").strip()
            student = next(
                (
                    record
                    for record in service.get_all_students()
                    if record["student_id"] == student_id
                ),
                None,
            )
            if student is None:
                print("Student ID not found.")
                logger.info("Update student failed: student ID not found.")
                continue

            print("Leave a field blank to keep its current value.")
            updates = {
                "name": input(f"Name [{student['name']}]: ").strip(),
                "course": input(f"Course [{student['course']}]: ").strip(),
                "year_level": input(
                    f"Year Level [{student['year_level']}]: "
                ).strip(),
            }
            updates = {
                field: value for field, value in updates.items() if value
            }
            if not updates:
                print("No changes made.")
                continue

            success, message = service.update_student(student_id, updates)
            print(message)
            logger.info("Update student result: %s", message)

        elif choice == "4":
            student_id = input("Enter Student ID to delete: ").strip()
            success, message = service.delete_student(student_id)
            print(message)
            logger.info("Delete student result: %s", message)

        elif choice == "5":
            print("Exiting...")
            logger.info("Application exited")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
