# Student Information System

A small command-line student information system that stores student records in
`data/students.json`.

## How to Run

From the `student-info-system` directory, run:

```console
python src/main.py
```

The application supports adding, viewing, updating, and deleting students.
When updating a student, leave a field blank to keep its current value.
Settings are read from `config/config.json`, and application activity is
written to `logs/app.log`.

## Project layout

- `src/models/student.py`: Student record model and JSON conversion helpers.
- `src/services/student_service.py`: JSON-backed student storage operations.
- `src/utils/logger.py`: Application file logger setup.
- `config/config.json`: Data file, log file, and application name settings.
- `data/students.json`: Student record storage.
