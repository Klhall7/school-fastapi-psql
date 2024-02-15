from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from db import session
from models import STUDENTS, ENROLLMENTS, COURSES

app= FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def home():
    return { "message": "Hello World!"}

@app.get('/students')
def select_students():
    student=session.query(STUDENTS)
    return student.all()
    
@app.get('/courses')
def select_courses():
    course=session.query(COURSES)
    return course.all()

@app.get('/enrollments')
def select_enrollments():
    enrollments=session.query(ENROLLMENTS, STUDENTS, COURSES).join(STUDENTS, STUDENTS.id == ENROLLMENTS.student_id).join(COURSES, COURSES.id == ENROLLMENTS.course_id)
    results = enrollments.all()
    enrollment_list = []
    for enrollment in results:
        enrollment_dict ={
            'enrollment_id': enrollment.ENROLLMENTS.enrollment_id,
            'student_name': enrollment.STUDENTS.name,
            'course_name': enrollment.COURSES.name,
            'enrollment_date': enrollment.ENROLLMENTS.enrollment_date
        }
        enrollment_list.append(enrollment_dict)
    return(enrollment_list)

@app.post('/create/student')
async def create_student(name: str):
    student=STUDENTS(name= name)
    session.add(student)
    session.commit()
    return {"Students added": student.name}

@app.post('/create/course')
async def create_course(name: str):
    course=COURSES(name= name)
    session.add(course)
    session.commit()
    return {"Courses added": course.name}

@app.post('/create/enrollment')
async def create_enrollment(student_id: int, course_id:int, enrollment_date:date):
    enrollment=ENROLLMENTS(student_id=student_id, course_id=course_id, enrollment_date = enrollment_date)
    session.add(enrollment)
    session.commit()
    return {"Enrollment added": enrollment.enrollment_id }

@app.put('/update/student/{id}')
async def update_student(id: int, name: str):
    student = session.query(STUDENTS).filter(STUDENTS.student_id == id).first()
    if student is not None:
        if name:
            student.name = name
        session.add(student)
        session.commit()
        return {"Updated Students": student.name}
    else:
        return {"message": "Student ID not found"}
    
@app.delete('/delete/enrollment/{id}')
async def remove_enrollment(id: int):
    exist_enrollment = session.query(ENROLLMENTS).filter(ENROLLMENTS.enrollment_id == id).first()
    if exist_enrollment is not None:
        session.delete(exist_enrollment)
        session.commit()
        return {"Deleted Enrollment": exist_enrollment.enrollment_id}
    else:
        return {"message": "Enrollment ID not found"}
