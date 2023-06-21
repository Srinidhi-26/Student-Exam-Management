# Installed Imports
from flask import request, Blueprint, url_for
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime as dt, timezone, date
import json

# Custom imports
from app import app, db
from app.models import StudentsMarks, Student


studentmarks_api = Blueprint(
    "studentmarks_api", __name__, url_prefix="/api/v1/student-marks"
)


class StudentsMarksException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@studentmarks_api.route("/", methods=["GET"])
@studentmarks_api.route("/<student_id>", methods=["GET"])
def get_student_marks(student_marks_id=None):
    now = dt.now(timezone.utc)
    all_marks = StudentsMarks.query
    page_num = request.args.get("page", 1, type=int)
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    search = request.args.get("search")
    marks = all_marks.order_by(getattr(getattr(StudentsMarks, sort), order)())
    if student_marks_id:
        student = all_marks.filter(StudentsMarks.id == student_marks_id).first()
        if not student:
            raise StudentsMarksException(
                f"Student ID {student_marks_id} doesn't exist.", 404
            )
    if search:
        all_marks = all_marks.filter(StudentsMarks.name.ilike(f"%{search}%"))
    paginated_marks = marks.paginate(page=page_num, error_out=False)
    all_marks = paginated_marks.items
    if paginated_marks.has_next:
        next_url = url_for(
            "studentmarks_api.get_student_marks", page=paginated_marks.next_num
        )
    else:
        next_url = None
    return {
        "success": True,
        "student_marks": all_marks,
        "timestamp": now,
        "message": "Students retrieved successfully.",
    }


@studentmarks_api.route("/", methods=["POST"])
def create_student_marks():
    now = dt.now(timezone.utc)
    student_id = request.json.get("student_id")
    name = request.json.get("name")
    sem1 = request.json.get("sem1")
    sem2 = request.json.get("sem2")
    sem3 = request.json.get("sem3")
    sem4 = request.json.get("sem4")

    create_student_marks = StudentsMarks(
        student_id=student_id, name=name, sem1=sem1, sem2=sem2, sem3=sem3, sem4=sem4
    )
    db.session.add(create_student_marks)
    db.session.commit()

    return {
        "success": True,
        "timestamp": now,
        "message": "Student marks successfully created",
    }, 201


@studentmarks_api.route("/", methods=["PUT"])
def update_student_marks():
    now = dt.now(timezone.utc)
    student_marks = request.get_json().get("student_marks")

    for student in student_marks:
        student_marks_id = student.get("student_marks_id")
        student_data = StudentsMarks.query.get(student_marks_id)

        if not student_data:
            raise StudentsMarksException(
                f"Students  ID {student_marks_id} doesn't exist.", 404
            )

        student_data.name = student.get("name", student_data.name)
        student_data.sem1 = student.get("sem1", student_data.sem1)
        student_data.sem2 = student.get("sem2", student_data.sem2)
        student_data.sem3 = student.get("sem3", student_data.sem3)
        student_data.sem4 = student.get("sem4", student_data.sem4)
        student_data.modify_time = now

    db.session.commit()

    return {
        "success": True,
        "timestamp": now,
        "message": "Student marks successfully updated",
    }


@studentmarks_api.route("/", methods=["DELETE"])
def delete_student_marks():
    now = dt.now(timezone.utc)
    student_marks_ids = request.get_json().get("student_marks_ids")
    delete_all = request.get_json().get("delete_all")
    if delete_all:
        StudentsMarks.query.delete()
    if not student_marks_ids:
        return {"message": "No student IDs provided"}, 400
    deleted_students = []
    for student_marks_id in student_marks_ids:
        student = StudentsMarks.query.get(student_marks_id)
        if not student:
            raise StudentsMarksException(
                f"Student ID {student_marks_id} doesn't exist.", 404
            )
        deleted_students.append(student)
        db.session.delete(student)
    db.session.commit()

    return {
        "success": True,
        "message": "Student's marks deleted successfully",
        "timestamp": now,
    }
