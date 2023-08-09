import random
from app import db

def fetch_courses() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Section;").fetchall()
    conn.close()
    course_list = []
    for result in query_results:
        item = {
            "CRN": result[2],
            "Course_Title": result[3],
            "GPA": result[5],
            "Instructor": result[6]
        }
        course_list.append(item)
    return course_list

def insert_course(Description: str) -> None:
    conn = db.connect()
    # Example input: CS,131,45,CS Madeup,13,3.5,Cristiano Ronaldo
    description_formatted = Description.split(",")
    if (len(description_formatted) >= 7):
        Subject = description_formatted[0]
        Course_Number = int(description_formatted[1])
        CRN = int(description_formatted[2])
        Course_Title = description_formatted[3]
        Course_Section = description_formatted[4]
        GPA = float(description_formatted[5])
        Instructor = description_formatted[6]
        query = 'Insert Into Section VALUES ("{}",{},{},"{}","{}",{},"{}");'.format(Subject,Course_Number,
            CRN,Course_Title,Course_Section,GPA,Instructor)
        conn.execute(query)
    conn.close()


def remove_course(CRN: int) -> None:
    """ remove entries based on CRN """
    conn = db.connect()
    query = 'Delete From Section where CRN={};'.format(CRN)
    conn.execute(query)
    conn.close()


def search_course(description: str) -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Section WHERE Primary_Instructor like '{}' or Course_Title like '{}' or CRN like {};").format(description,description,description).fetchall()
    conn.close()
    course_list = []
    for result in query_results:
        item = {
            "CRN": result[2],
            "Course_Title": result[3],
            "GPA": result[5],
            "Instructor": result[6]
        }
        course_list.append(item)
    return course_list

def update_course(CRN: int, GPA:float) -> None:
    conn = db.connect()
    print(CRN,GPA)
    query = 'Update Section set Average_Grade = {} where CRN = {};'.format(GPA, CRN)
    conn.execute(query)
    conn.commit()
    conn.close()
    
    
def find_recom_course() -> dict:
    # print(Subject)
    conn = db.connect()
    query = '''SELECT DISTINCT d.CRN, i.name, i.average_rating, s.Subject, s.Average_Grade, s.Course_Title, s.Course
FROM Disparity d NATURAL JOIN Instructor i NATURAL JOIN Section s
WHERE (d.A >= (d.A + d.B + d.C + d.D + d.F) * .9) AND (s.Course LIKE '4%%') AND (i.average_rating >= 4) AND (s.Subject = 'CS')
GROUP BY d.CRN, i.name, i.average_rating, s.Subject, s.Average_Grade, s.Course_Title, s.Course
ORDER BY i.average_rating DESC, d.CRN
LIMIT 15;'''
    query_results = conn.execute(query)
    # print(results.all())
    conn.close()
    course_list = []
    for result in query_results:
        item = {
            "CRN": result[0],
            "Course_Title": result[5],
            "GPA": result[4],
            "Instructor": result[1]
            }
        course_list.append(item)
    return course_list
    
    
def find_general_best_courses() -> dict:
    conn = db.connect()
    query = '''SELECT s.CRN, s.Primary_Instructor, s.Average_Grade, s.Course, s.Course_Title, AVG(r.student_rating) as avg_rat, AVG(r.student_difficulty) as avg_diff
FROM Section s NATURAL JOIN Ratings r
WHERE (s.Course LIKE '4%%') AND (s.Average_Grade >= 3.5)
GROUP BY s.CRN, s.Primary_Instructor, s.Average_Grade, s.Course, s.Course_Title HAVING avg_rat >= 3.5 AND avg_diff < 3
ORDER BY avg_rat ASC, avg_diff DESC
LIMIT 15;'''
    query_results = conn.execute(query)
    conn.close()
    course_list = []
    for result in query_results:
        item = {
            "CRN": result[0],
            "Course_Title": result[4],
            "GPA": result[2],
            "Instructor": result[1]
            }
        course_list.append(item)
    return course_list
