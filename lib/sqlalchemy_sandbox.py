#!/usr/bin/env python3
import os
os.environ['SQLALCHEMY_WARN_20'] = '1'
from datetime import datetime
from sqlalchemy import create_engine, Column, DateTime, Integer, String, PrimaryKeyConstraint, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Use declarative_base from sqlalchemy.ext.declarative
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id_pk'),
        UniqueConstraint('email', name='unique_email'),
        CheckConstraint('grade BETWEEN 1 AND 12', name='grade_between_1_and_12')
    )

    # Define an Index for the 'name' column
    Index('index_name', 'name')

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))  # Increased the length of the name field
    email = Column(String(255))  # Increased the length of the email field
    grade = Column(Integer)
    birthday = Column(DateTime)
    enrolled_date = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"Student {self.id}: {self.name}, Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///mydatabase.db')  # Use a file-based SQLite database
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(year=1879, month=3, day=14),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(year=1912, month=6, day=23),
    )

    session.add_all([albert_einstein, alan_turing])  # Use add_all to add multiple objects
    session.commit()

    students = session.query(Student).all()  # Use .all() to fetch all records

    for student in students:
        print(student)

    # Now you can access the ID after committing:
    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")
