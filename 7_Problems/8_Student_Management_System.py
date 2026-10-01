'''

Student Management System v2

Build a complete command-line Student Management System.

Features
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
Initial Data

Start with:

id,name,python,sql,dsa
101,Arsh,85,78,92
102,Rahul,72,88,75
103,Aman,95,91,89
104,Vijay,60,68,64
105,Neha,82,79,85

Program Requirements

### Use:
- Functions
- Lists
- Dictionaries
- CSV
- Exception handling
- Decorators
- Generators

### Functions to consider
- load_students()
- save_students()
- add_student()
- update_student()
- delete_student()
- search_student()
- display_students()
- calculate_average()
- generate_statistics()
- export_report()
- main()

### Test Operations

> Add:
ID: 106
Name: Priya
Python: 91
SQL: 87
DSA: 94

> Update:
Student ID: 104

New Python mark: 70
New SQL mark: 74
New DSA mark: 72

> Search:
Student ID: 103

> Delete:
Student ID: 102

### Statistics

> Generate:
- Highest scorer
- Lowest scorer
- Class average
- Subject toppers
- Students who passed
- Top 3 students

### Additional Requirements

Use exception handling for:
- Invalid student ID
- Duplicate student ID
- Invalid marks
- Missing CSV file
- Student not found
- Non-numeric input

### Use a decorator for:
Logging function calls

Use another decorator for:
Execution timing

Use a generator when processing student records from the CSV.

The final system should continue running until the user chooses:

8. Exit

'''

import csv
import os
import time
from functools import wraps

FILENAME = "C:\\Users\\Mohd Arsh\\Python_Workspace\\7_Problems\\studentfinal.csv"


# ============================================================
# DECORATORS
# ============================================================

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} finished")
        return result
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


# ============================================================
# GENERATOR + LOAD / SAVE
# ============================================================

def read_student_rows(filename):
    """Generator: yields one student row at a time from CSV"""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def load_students():
    """Load all students from CSV into a list of dictionaries"""
    if not os.path.exists(FILENAME):
        print("CSV file not found. Creating a new one...")
        return []

    students = []
    try:
        for row in read_student_rows(FILENAME):
            students.append({
                "id": int(row["id"]),
                "name": row["name"].strip(),
                "python": int(row["python"]),
                "sql": int(row["sql"]),
                "dsa": int(row["dsa"])
            })
    except Exception as e:
        print(f"Error loading students: {e}")
        return []

    return students


def save_students(students):
    """Save list of students back to CSV"""
    try:
        with open(FILENAME, "w", newline="") as file:
            fieldnames = ["id", "name", "python", "sql", "dsa"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
    except Exception as e:
        print(f"Error saving students: {e}")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_average(student):
    return round((student["python"] + student["sql"] + student["dsa"]) / 3, 2)


def get_valid_marks(subject):
    """Get valid marks (0-100) from user"""
    while True:
        try:
            marks = int(input(f"Enter {subject} marks (0-100): "))
            if 0 <= marks <= 100:
                return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def find_student_by_id(students, student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


# ============================================================
# MAIN FEATURES
# ============================================================

@logger
@timer
def add_student(students):
    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print("Invalid ID. Must be a number.")
        return

    # Check duplicate ID
    if find_student_by_id(students, student_id):
        print(f"Student ID {student_id} already exists.")
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    python = get_valid_marks("Python")
    sql = get_valid_marks("SQL")
    dsa = get_valid_marks("DSA")

    new_student = {
        "id": student_id,
        "name": name,
        "python": python,
        "sql": sql,
        "dsa": dsa
    }

    students.append(new_student)
    save_students(students)
    print("Student added successfully!")


@logger
@timer
def update_student(students):
    try:
        student_id = int(input("Enter Student ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    print(f"Updating marks for {student['name']}")
    student["python"] = get_valid_marks("Python")
    student["sql"] = get_valid_marks("SQL")
    student["dsa"] = get_valid_marks("DSA")

    save_students(students)
    print("Student updated successfully!")


@logger
@timer
def delete_student(students):
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    students.remove(student)
    save_students(students)
    print(f"Student {student['name']} deleted successfully!")


@logger
def search_student(students):
    try:
        student_id = int(input("Enter Student ID to search: "))
    except ValueError:
        print("Invalid ID.")
        return

    student = find_student_by_id(students, student_id)
    if not student:
        print("Student not found.")
        return

    avg = calculate_average(student)
    print("\n--- Student Found ---")
    print(f"ID     : {student['id']}")
    print(f"Name   : {student['name']}")
    print(f"Python : {student['python']}")
    print(f"SQL    : {student['sql']}")
    print(f"DSA    : {student['dsa']}")
    print(f"Average: {avg}")


@logger
def display_students(students):
    if not students:
        print("No students found.")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<6} {'Name':<12} {'Python':<8} {'SQL':<8} {'DSA':<8} {'Average':<8}")
    print("=" * 70)

    for student in students:
        avg = calculate_average(student)
        print(f"{student['id']:<6} {student['name']:<12} {student['python']:<8} "
              f"{student['sql']:<8} {student['dsa']:<8} {avg:<8}")
    print("=" * 70)


@logger
@timer
def generate_statistics(students):
    if not students:
        print("No students available for statistics.")
        return

    print("\n" + "=" * 50)
    print("           CLASS STATISTICS")
    print("=" * 50)

    # Highest & Lowest scorer
    highest = max(students, key=calculate_average)
    lowest = min(students, key=calculate_average)
    print(f"Highest Scorer : {highest['name']} ({calculate_average(highest)})")
    print(f"Lowest Scorer  : {lowest['name']} ({calculate_average(lowest)})")

    # Class average
    class_avg = sum(calculate_average(s) for s in students) / len(students)
    print(f"Class Average  : {round(class_avg, 2)}")

    # Subject toppers
    print("\n--- Subject Toppers ---")
    for subject in ["python", "sql", "dsa"]:
        topper = max(students, key=lambda s: s[subject])
        print(f"{subject.upper():<7} Topper: {topper['name']} ({topper[subject]})")

    # Passing students (average >= 70)
    passing = [s["name"] for s in students if calculate_average(s) >= 70]
    print(f"\nStudents who passed: {', '.join(passing) if passing else 'None'}")

    # Top 3 students
    top3 = sorted(students, key=calculate_average, reverse=True)[:3]
    print("\n--- Top 3 Students ---")
    for i, s in enumerate(top3, start=1):
        print(f"{i}. {s['name']} - Average: {calculate_average(s)}")

    print("=" * 50)


@logger
@timer
def export_report(students):
    if not students:
        print("No data to export.")
        return

    try:
        with open("student_report.txt", "w") as file:
            file.write("STUDENT REPORT\n")
            file.write("=" * 50 + "\n")

            for student in students:
                avg = calculate_average(student)
                file.write(f"ID: {student['id']} | Name: {student['name']} | "
                           f"Python: {student['python']} | SQL: {student['sql']} | "
                           f"DSA: {student['dsa']} | Average: {avg}\n")

            file.write("=" * 50 + "\n")

        print("Report exported successfully to 'student_report.txt'")
    except Exception as e:
        print(f"Error exporting report: {e}")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    students = load_students()

    while True:
        print("\n" + "=" * 40)
        print("     STUDENT MANAGEMENT SYSTEM v2")
        print("=" * 40)
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Display Students")
        print("6. Generate Statistics")
        print("7. Export Report")
        print("8. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            delete_student(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            display_students(students)
        elif choice == "6":
            generate_statistics(students)
        elif choice == "7":
            export_report(students)
        elif choice == "8":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()



'''
OUTPUT:

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 5
[LOG] Calling display_students

======================================================================
ID     Name         Python   SQL      DSA      Average 
======================================================================
101    Arsh         85       78       92       85.0    
102    Rahul        72       88       75       78.33   
103    Aman         95       91       89       91.67   
104    Vijay        60       68       64       64.0    
105    Neha         82       79       85       82.0    
======================================================================
[LOG] display_students finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 1
[LOG] Calling add_student
Enter Student ID: 106
Enter Name: Priya
Enter Python marks (0-100): 91
Enter SQL marks (0-100): 87
Enter DSA marks (0-100): 94
Student added successfully!
[TIMER] add_student took 12.428314 seconds
[LOG] add_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 5
[LOG] Calling display_students

======================================================================
ID     Name         Python   SQL      DSA      Average 
======================================================================
101    Arsh         85       78       92       85.0    
102    Rahul        72       88       75       78.33   
103    Aman         95       91       89       91.67   
104    Vijay        60       68       64       64.0    
105    Neha         82       79       85       82.0    
106    Priya        91       87       94       90.67   
======================================================================
[LOG] display_students finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 2
[LOG] Calling update_student
Enter Student ID to update: 104
Updating marks for Vijay
Enter Python marks (0-100): 70
Enter SQL marks (0-100): 74
Enter DSA marks (0-100): 72
Student updated successfully!
[TIMER] update_student took 8.455415 seconds
[LOG] update_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 4
[LOG] Calling search_student
Enter Student ID to search: 103

--- Student Found ---
ID     : 103
Name   : Aman
Python : 95
SQL    : 91
DSA    : 89
Average: 91.67
[LOG] search_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 3
[LOG] Calling delete_student
Enter Student ID to delete: 102
Student Rahul deleted successfully!
[TIMER] delete_student took 1.919601 seconds
[LOG] delete_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 5
[LOG] Calling display_students

======================================================================
ID     Name         Python   SQL      DSA      Average 
======================================================================
101    Arsh         85       78       92       85.0    
103    Aman         95       91       89       91.67   
104    Vijay        70       74       72       72.0    
105    Neha         82       79       85       82.0    
106    Priya        91       87       94       90.67   
======================================================================
[LOG] display_students finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 6
[LOG] Calling generate_statistics

==================================================
           CLASS STATISTICS
==================================================
Highest Scorer : Aman (91.67)
Lowest Scorer  : Vijay (72.0)
Class Average  : 84.27

--- Subject Toppers ---
PYTHON  Topper: Aman (95)
SQL     Topper: Aman (91)
DSA     Topper: Priya (94)

Students who passed: Arsh, Aman, Vijay, Neha, Priya

--- Top 3 Students ---
1. Aman - Average: 91.67
2. Priya - Average: 90.67
3. Arsh - Average: 85.0
==================================================
[TIMER] generate_statistics took 0.003054 seconds
[LOG] generate_statistics finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 7
[LOG] Calling export_report
Report exported successfully to 'student_report.txt'
[TIMER] export_report took 0.001455 seconds
[LOG] export_report finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 9
Invalid choice. Please enter a number between 1 and 8.

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 1
[LOG] Calling add_student
Enter Student ID: 101
Student ID 101 already exists.
[TIMER] add_student took 3.929966 seconds
[LOG] add_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 4
[LOG] Calling search_student
Enter Student ID to search: 999
Student not found.
[LOG] search_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 3
[LOG] Calling delete_student
Enter Student ID to delete: 999
Student not found.
[TIMER] delete_student took 2.176882 seconds
[LOG] delete_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 1
[LOG] Calling add_student
Enter Student ID: 107
Enter Name: Ravi
Enter Python marks (0-100): 150
Marks must be between 0 and 100.
Enter Python marks (0-100): 85
Enter SQL marks (0-100): 91
Enter DSA marks (0-100): 78
Student added successfully!
[TIMER] add_student took 31.194278 seconds
[LOG] add_student finished

========================================
     STUDENT MANAGEMENT SYSTEM v2
========================================
1. Add Student
2. Update Student
3. Delete Student
4. Search Student
5. Display Students
6. Generate Statistics
7. Export Report
8. Exit
========================================
Enter your choice (1-8): 8
Exiting Student Management System. Goodbye!
========================================

Expected Final Students (after all operations)

ID,Name,Python,SQL,DSA
101,Arsh,85,78,92
103,Aman,95,91,89
104,Vijay,70,74,72
105,Neha,82,79,85
106,Priya,91,87,94

(Rahul deleted, Vijay updated, Priya added)
'''