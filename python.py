import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
''')

# Function to list students enrolled in "Database Systems"
def list_students_in_course(course_name):
    cursor.execute("SELECT name FROM students WHERE course = ?", (course_name,))
    students = cursor.fetchall()
    if students:
        print(f"Students enrolled in '{course_name}':")
        for student in students:
            print(student[0])
    else:
        print(f"No students are enrolled in '{course_name}'.")

# Function to add a new student
def add_student(name, age, course):
    cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
    connection.commit()
    print(f"Added student: {name}, Age: {age}, Course: {course}")

# Function to update the age of a student by student_id
def update_student_age(student_id, new_age):
    cursor.execute("UPDATE students SET age = ? WHERE student_id = ?", (new_age, student_id))
    connection.commit()
    print(f"Updated age of student with ID {student_id} to {new_age}.")

# Example usage
if __name__ == "__main__":
    # Add sample data (uncomment if needed)
    # add_student("Alice", 22, "Database Systems")
    # add_student("Bob", 24, "Operating Systems")
    # add_student("Charlie", 23, "Database Systems")

    # List students in the "Database Systems" course
    list_students_in_course("Database Systems")

    # Add a new student
    add_student("David", 25, "Database Systems")

    # Update the age of a student
    update_student_age(1, 26)  # Update student with ID 1

    # List students again to confirm changes
    list_students_in_course("Database Systems")

# Close the database connection when done
connection.close()