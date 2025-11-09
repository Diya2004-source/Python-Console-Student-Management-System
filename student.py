import os
import sqlite3

class College:
    def __init__(self):
        # Ensure the database folder exists
        os.makedirs("data", exist_ok=True)
        self.con = sqlite3.connect(r"data/student.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        self.create_table()

    # ------------------ Tables ------------------ #
    def create_table(self):
        # Students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students(
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                stream TEXT,
                contact INTEGER
            )
        ''')
        # Marks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Marks(
                marks_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT NOT NULL,
                marks INTEGER,
                FOREIGN KEY(student_id) REFERENCES Students(student_id) ON DELETE CASCADE
            )
        ''')
        self.con.commit()

    # ------------------ Students CRUD ------------------ #
    def add_student(self):   
        name = input("Enter student name: ")
        age = int(input("Enter age: "))
        stream = input("Enter class/stream: ")
        contact = int(input("Enter contact number: "))

        self.cursor.execute(
            "INSERT INTO Students (name, age, stream, contact) VALUES (?,?,?,?)",
            (name, age, stream, contact)  #insert query in table
        )
        self.con.commit() #use to save work
        print("Student added successfully!")

    def update_student(self):
        student_id = int(input("Enter Student ID to update: "))
        self.cursor.execute("SELECT * FROM Students WHERE student_id=?", (student_id,))  #update query
        student = self.cursor.fetchone()
        if not student:   #check that if recrord is in the table or not
            print("Student not found!")
            return

        print("Which field do you want to update?") #if yes the it will ask what you want to update 
        print("1. Name\n2. Age\n3. Stream\n4. Contact")
        choice = input("Enter number: ")

        if choice == '1':
            new_value = input("Enter new name: ")
            self.cursor.execute("UPDATE Students SET name=? WHERE student_id=?", (new_value, student_id))
        elif choice == '2':
            new_value = int(input("Enter new age: "))
            self.cursor.execute("UPDATE Students SET age=? WHERE student_id=?", (new_value, student_id))
        elif choice == '3':
            new_value = input("Enter new stream: ")
            self.cursor.execute("UPDATE Students SET stream=? WHERE student_id=?", (new_value, student_id))
        elif choice == '4':
            new_value = int(input("Enter new contact: "))
            self.cursor.execute("UPDATE Students SET contact=? WHERE student_id=?", (new_value, student_id))
        else:
            print("Invalid choice!")
            return

        self.con.commit()
        print("Student updated successfully!")

    def delete_student(self):
        student_id = int(input("Enter Student ID to delete: "))
        self.cursor.execute("SELECT * FROM Students WHERE student_id=?", (student_id,)) 
        student = self.cursor.fetchone()
        if not student:
            print("Student not found!")
            return

        confirm = input(f"Are you sure you want to delete student {student_id}? (yes/no): ").lower()
        if confirm == 'yes':
            self.cursor.execute("DELETE FROM Students WHERE student_id=?", (student_id,)) #delete query
            self.con.commit()
            print("Student deleted successfully!")
        else:
            print("Deletion cancelled.")

    def view_students(self):
        self.cursor.execute("SELECT * FROM Students") #select query
        rows = self.cursor.fetchall()
        if rows:
            print("\n--- Students List ---")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Stream: {row[3]}, Contact: {row[4]}")
        else:
            print("No students found.")

    # ------------------ Marks CRUD ------------------ #
    def add_marks(self):
        student_id = int(input("Enter Student ID to add marks for: "))
        self.cursor.execute("SELECT * FROM Students WHERE student_id=?", (student_id,)) #show records of student table
        student = self.cursor.fetchone()
        if not student:
            print("Student not found!")
            return

        subject = input("Enter subject name: ")
        marks = int(input("Enter marks: "))

        self.cursor.execute(
            "INSERT INTO Marks (student_id, subject, marks) VALUES (?,?,?)",
            (student_id, subject, marks) #insert records into marks table
        )
        self.con.commit()
        print("Marks added successfully!")

    def update_marks(self):
        marks_id = int(input("Enter Marks ID to update: "))
        self.cursor.execute("SELECT * FROM Marks WHERE marks_id=?", (marks_id,)) #update query
        record = self.cursor.fetchone()
        if not record:
            print("Record not found!")
            return

        print("Which field do you want to update?") #what u want to update
        print("1. Subject\n2. Marks")
        choice = input("Enter number: ")

        if choice == '1':
            new_subject = input("Enter new subject name: ")
            self.cursor.execute("UPDATE Marks SET subject=? WHERE marks_id=?", (new_subject, marks_id))
        elif choice == '2':
            new_marks = int(input("Enter new marks: "))
            self.cursor.execute("UPDATE Marks SET marks=? WHERE marks_id=?", (new_marks, marks_id))
        else:
            print("Invalid choice!")
            return

        self.con.commit()
        print("Marks updated successfully!")

    def delete_marks(self):
        marks_id = int(input("Enter Marks ID to delete: "))
        self.cursor.execute("SELECT * FROM Marks WHERE marks_id=?", (marks_id,)) #delete
        record = self.cursor.fetchone()
        if not record:
            print("Record not found!")
            return

        confirm = input("Are you sure you want to delete this record? (yes/no): ").lower()
        if confirm == 'yes':
            self.cursor.execute("DELETE FROM Marks WHERE marks_id=?", (marks_id,))
            self.con.commit()
            print("Marks record deleted successfully!")
        else:
            print("Deletion cancelled.")

    def view_marks(self):
        self.cursor.execute('''
            SELECT Marks.marks_id, Students.name, Marks.subject, Marks.marks
            FROM Marks
            INNER JOIN Students ON Marks.student_id = Students.student_id
        ''')   # join query to see records
        rows = self.cursor.fetchall()
        if rows:
            print("\n--- Marks List ---")
            for row in rows:
                print(f"Marks ID: {row[0]}, Student: {row[1]}, Subject: {row[2]}, Marks: {row[3]}")
        else:
            print("No marks records found.")

    # ------------------ Main Menu ------------------ #
    def run(self):
        while True:
            print("\n--- Student Management System ---")
            print("1. Add Student")
            print("2. Update Student")
            print("3. Delete Student")
            print("4. View Students")
            print("5. Add Marks")
            print("6. Update Marks")
            print("7. Delete Marks")
            print("8. View Marks")
            print("9. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.update_student()
            elif choice == '3':
                self.delete_student()
            elif choice == '4':
                self.view_students()
            elif choice == '5':
                self.add_marks()
            elif choice == '6':
                self.update_marks()
            elif choice == '7':
                self.delete_marks()
            elif choice == '8':
                self.view_marks()
            elif choice == '9':
                print("Exiting program...")
                break
            else:
                print("Invalid choice! Please try again.")

# ------------------ Run the program ------------------ #
if __name__ == "__main__":
    College().run()
