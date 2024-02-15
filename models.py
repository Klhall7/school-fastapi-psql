from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import declarative_base
from db import engine

Base=declarative_base()

class STUDENTS(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
class COURSES(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
class ENROLLMENTS(Base):
    __tablename__ ="enrollments"
    
    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrollment_date = Column(Date)

Base.metadata.create_all(engine)