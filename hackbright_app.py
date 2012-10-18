import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name,last_name,github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name,last_name)

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Max Grade: %d""" %(row[0], row[1], row[2])

def make_new_project(title,description,max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added student: %s %s %s" %(title,description,max_grade)

def get_grade_by_project(github,title):
    query = """SELECT grades FROM Grades WHERE student_github = ? and project_title = ?"""
    DB.execute(query, (github,title))
    row = DB.fetchone()
    print """\
Student: %s
Project: %s
Grade: %d""" %(github,title,row[0])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade":
            get_grade_by_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
