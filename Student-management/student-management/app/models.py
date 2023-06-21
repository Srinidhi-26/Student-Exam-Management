# Builtin Imports
from datetime import datetime, timezone, date
from dataclasses import dataclass
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Custom Imports
from app import db


@dataclass
class Student(db.Model):
    id: UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = db.Column(db.Text, nullable=False)
    email: str = db.Column(db.Text, nullable=False)
    gender: str = db.Column(db.Text, nullable=False)
    stream: str = db.Column(db.Text, nullable=False)
    address: str = db.Column(db.Text, nullable=False)
    yop: int = db.Column(db.Integer, nullable=False)

    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: datetime = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )


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
