from datetime import datetime as dt, timezone
from flask import Blueprint, request, session, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone
from sqlalchemy.dialects.postgresql import UUID
from flask import request
from datetime import datetime as dt
from app import db
from app.models import Student, StudentsMarks
import uuid


studentmanagement_api = Blueprint(
    "studentmanagement_api", __name__, url_prefix="/api/v1/student"
)


class StudentException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@studentmanagement_api.route("/", methods=["GET"])
@studentmanagement_api.route("/<student_id>", methods=["GET"])
def get_student(student_id=None):
    now = dt.now(timezone.utc)
    all_students = Student.query
    page_num = request.args.get("page", 1, type=int)
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    search = request.args.get("search")
    students = all_students.order_by(getattr(getattr(Student, sort), order)())
    if student_id:
        student = all_students.filter(Student.id == student_id).first()
        if not student:
            raise StudentException(f"Student ID {student_id} doesn't exist.", 404)
    if search:
        all_students = all_students.filter(Student.name.ilike(f"%{search}%"))
    paginated_students = students.paginate(page_num, False)
    all_students = paginated_students.items
    next_url = (
        url_for("studentmanagement_api.get_student", page=paginated_students.next_num)
        if paginated_students.has_next
        else None
    )
    return {
        "success": True,
        "students": all_students,
        "timestamp": now,
        "page": paginated_students.page,
        "next_page": next_url,
        "total_pages": paginated_students.pages,
        "total": paginated_students.total,
        "message": "Students retrieved successfully.",
    }


@studentmanagement_api.route("/add", methods=["POST"])
def create_student():
    now = dt.now(timezone.utc)
    data = request.json
    name = data.get("name")
    email = data.get("email")
    gender = data.get("gender")
    stream = data.get("stream")
    address = data.get("address")
    yop = data.get("yop")
    new_student = Student(
        name=name,
        email=email,
        gender=gender,
        stream=stream,
        address=address,
        yop=yop,
    )
    db.session.add(new_student)
    db.session.commit()
    return {
        "success": True,
        "timestamp": now,
        "message": "Student created successfully.",
    }, 201


@studentmanagement_api.route("/update", methods=["PUT"])
def update_student():
    now = dt.now(timezone.utc)
    data = request.json
    students = data.get("students", [])
    for student_data in students:
        student_id = student_data.get("student_id")
        student = Student.query.get(student_id)
        if not student:
            raise StudentException(f"Student ID {student_id} doesn't exist.", 404)
        student.name = student_data.get("name", student.name)
        student.email = student_data.get("email", student.email)
        student.address = student_data.get("address", student.address)
        student.modify_time = now
    db.session.commit()
    return {
        "success": True,
        "timestamp": now,
        "message": "Students updated successfully.",
    }


@studentmanagement_api.route("/delete", methods=["DELETE"])
def delete_students():
    now = dt.now(timezone.utc)
    data = request.get_json()
    student_ids = data.get("student_ids", [])
    delete_all = data.get("delete_all", False)
    if delete_all:
        Student.query.delete()
    if not student_ids:
        return {"message": "No Student IDs are provided"}, 400
    deleted_students = []
    for student_id in student_ids:
        student = Student.query.get(student_id)
        if not student:
            raise StudentException(f"Student ID {student_id} doesn't exist.", 404)
        deleted_students.append(student)
        db.session.delete(student)
    db.session.commit()
    return {
        "success": True,
        "message": "Students deleted successfully.",
        "timestamp": now,
    }
