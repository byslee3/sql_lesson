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

def overwrite_old_grade(github, title, new_grade):
    query = """UPDATE Grades set grades = ? WHERE student_github = ? and project_title = ? """
    DB.execute(query, (new_grade, github, title))
    CONN.commit()
    print "Successfully changed grade: %s %s %s" %(new_grade, github, title)

def get_all_grades(github):

    query = """SELECT * FROM Grades WHERE student_github = ?"""

    for row in DB.execute(query, (github,)):
        print "Student: %s --- Project: %s --- Grade: %d" %(row[0],row[1],row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    next_command = None
    while command != "quit" and next_command != "quit" and next_command != "n":

        ### Need to also add validation -- if someone enters arguments into a query, but it's not in the table
        ### Currently it crashes because it can't find the record in the SQL database
        ### We should modify it so that it returns a message "No record found"
        ### Do this in each of the individual functions

        print "Which command would you like to do?"
        print "1 --> Find a student"
        print "2 --> Add a new student"
        print "3 --> Find a project"
        print "4 --> Add a new project"
        print "5 --> Find all of a student's grades"
        print "6 --> Find a student's grade on a particular project"
        print "7 --> Overwrite a student's grade on a particular project"

        command = raw_input("HBA Database> ")

        #Is there a simpler way to do this? This seems to be a common case.
        if command == '1' or command == '2' or command == '3' or command == '4' or command == '5' or command == '6' or command == '7':
            numeric_command = int(command)     
        
        if numeric_command == 1:
            github = raw_input("What is the student's Github account name? ")
            get_student_by_github(github)
        elif numeric_command == 2:
            first_name = raw_input("What is the student's first name? ")
            last_name = raw_input("What is the student's last name? ")
            github = raw_input("What is the student's Github account name? ")
            make_new_student(first_name,last_name,github)
        elif numeric_command == 3:
            title = raw_input("What is the title of the project? ")
            get_project_by_title(title)
        elif numeric_command == 4:
            title = raw_input("What is the title of the project? ")
            description = raw_input("Please describe the project: ")
            max_grade = raw_input("What is the max grade on the project? ")
            make_new_project(title,description,max_grade)
        elif numeric_command == 5:
            github = raw_input("What is the student's Github account name? ")
            get_all_grades(github)
        elif numeric_command == 6:
            github = raw_input("What is the student's Github account name? ")
            title = raw_input("Which project are you looking for? ")
            get_grade_by_project(github,title)
        elif numeric_command == 7:
            github = raw_input("What is the student's Github account name? ")
            title = raw_input("Which project are you changing the grade for? ")
            new_grade = int(raw_input("What is the new grade? "))
            overwrite_old_grade(github, title, new_grade)

        next_command = raw_input("Continue? ")

        #input_string = raw_input("HBA Database> ")
        #tokens = input_string.split(",")
        #command = tokens[0]
        #args = tokens[1:]
    

    CONN.close()

if __name__ == "__main__":
    main()
