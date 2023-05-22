from app import db
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timezone
from sqlalchemy.dialects.postgresql import UUID
from flask import request
from datetime import datetime as dt
import uuid
import json


class UTCDateTime(db.TypeDecorator):
    """Make datetime objects store timezone info and always in UTC"""

    impl = db.DateTime(timezone=True)
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return value.astimezone(tz=timezone.utc)


@dataclass
class Student(db.Model):
    id: UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = db.Column(db.Text, nullable=False)
    email: str = db.Column(db.Text, nullable=False)
    Phone_no: int = db.Column(db.Integer, nullable=False)
    Gender: str = db.Column(db.Text, nullable=False)
    stream: str = db.Column(db.Text, nullable=False)
    address: str = db.Column(db.Text, nullable=False)
    yop: int = db.Column(db.Integer, nullable=False)
    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: datetime = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )

    def get_editable_fields(self):
        return ("name", "email", "Phone_no", "address")

    def get_sort_fields(self):
        return ("name", "Gender", "stream")


@dataclass
class StudentsMarks(db.Model):
    id: UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: str = db.Column(db.Text)
    name: str = db.Column(db.Text, nullable=False)
    sem1: int = db.Column(db.Integer, nullable=False)
    sem2: int = db.Column(db.Integer, nullable=False)
    sem3: int = db.Column(db.Integer, nullable=False)
    sem4: int = db.Column(db.Integer, nullable=False)
    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: datetime = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )

    def get_editable_fields(self):
        return ("name", "sem1", "sem2", "sem3", "sem4")

    def get_sort_fields(self):
        return ("name", "sem1", "sem2", "sem3", "sem4")
