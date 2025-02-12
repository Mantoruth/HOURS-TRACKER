from __future__ import annotations
from typing import List
from sqlalchemy import create_engine, Column, ForeignKey, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session

engine = create_engine("sqlite:///hrs_tracker.db", echo=True)

class Base(DeclarativeBase):
    pass

class Subject(Base):
    __tablename__ = "subjects"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))  # Specify length
    classes: Mapped[List["Class"]] = relationship(
        "Class",
        secondary="class_subjects",
        back_populates="subjects"
    )

class Class(Base):
    __tablename__ = "classes"

    id = mapped_column(Integer, primary_key=True)
    classname = mapped_column(String(50), unique=True)  # Specify length
    level = mapped_column(Integer)
    subjects: Mapped[List[Subject]] = relationship(
        "Subject",
        secondary="class_subjects",
        back_populates="classes"
    )

class ClassSubject(Base):
    __tablename__ = "class_subjects"
    
    class_id = mapped_column(Integer, ForeignKey("classes.id"), primary_key=True)
    subject_id = mapped_column(Integer, ForeignKey("subjects.id"), primary_key=True)
    
    def __repr__(self):
        return f"<ClassSubject(subject_id={self.subject_id}, name='{self.name}')>"
        
class Teacher(Base):
    __tablename__ = 'teachers'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)  # Specify length
    total_hours = mapped_column(Integer)
    hours_taught = mapped_column(Integer)
    hours_left = mapped_column(Integer)

class Record(Base):
    __tablename__ = "records"

    id = mapped_column(Integer, primary_key=True)
    date = mapped_column(Date)
    hours_taught = mapped_column(Integer)
    class_subject_id = mapped_column(ForeignKey("class_subjects.class_id"))

class HoursRecord(Base):
    __tablename__ = "hours_records"

    id = mapped_column(Integer, primary_key=True)
    teacher_id = mapped_column(Integer, ForeignKey("teachers.id"))
    class_subject_id = mapped_column(Integer, ForeignKey("class_subjects.class_id"))
    hours_taught = mapped_column(Integer)
    date = mapped_column(Date)

class ClassRecord(Base):
    __tablename__ = "class_records"

    id = mapped_column(Integer, primary_key=True)
    subject_id = mapped_column(Integer, ForeignKey("class_subjects.subject_id"))  # Foreign key for subject
    class_name = mapped_column(String)  # Name of the class
    date = mapped_column(Date)  # Date of the class
    number_of_hours = mapped_column(Integer)  # Duration in hours

    def __repr__(self):
        return (f"<ClassRecord(id={self.id}, subject_id={self.subject_id}, "
                f"class_name='{self.class_name}', date={self.date}, "
                f"number_of_hours={self.number_of_hours})>")


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        subjects = ["Advanced Python Programming", "Data Analysis", "Advanced Object-Oriented Programming", "Introduction to Artificial Intelligence"]
        classes = {
            1: ["Ba1A", "Ba1B", "Ba1C", "Ba1D"],
            2: ["Ba2A", "Ba2B"],
            3: ["SE3A", "SE3B"]
        }
        teachers = ["Nguh Prince"]

        # Add subjects
        for subject in subjects:
            new_subject = Subject(name=subject)
            session.add(new_subject)

        # Add classes
        for level, classnames in classes.items():
            for classname in classnames:
                session.add(Class(classname=classname.upper(), level=level))

        # Add teachers
        for teacher in teachers:
            session.add(Teacher(name=teacher))

        # Commit all additions at once
        session.commit()