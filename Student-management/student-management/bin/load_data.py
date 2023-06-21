#!/usr/bin/env python3
import os
import sys
import json
from app.models import Student, StudentsMarks


def save_students_to_json():
    students = Student.query
    student_data = []
    for student in students:
        student_dict = {
            "id": str(student.id),
            "name": student.name,
            "email": student.email,
            "gender": student.gender,
            "stream": student.stream,
            "yop": student.yop,
        }
        student_data.append(student_dict)
    json_data = json.dumps(student_data)
    with open("student.json", "w") as file:
        file.write(json_data)
    return {"message: Data added"}


save_students_to_json()


def save_students_to_json():
    students = StudentsMarks.query
    student_data = []
    for student in students:
        student_dict = {
            "id": (student.id),
            "name": student.name,
            "sem1": student.sem1,
            "sem2": student.sem2,
            "sem3": student.sem3,
            "sem4": student.sem4,
        }
        student_data.append(student_dict)
    json_data = json.dumps(student_data)
    with open("student_marks.json", "w") as file:
        file.write(json_data)
    return {"message: Data added"}


save_students_to_json
