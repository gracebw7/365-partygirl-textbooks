
from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

from src.api.courses import Course, create_course
from src.api.professors import Professor, create_professor

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Class(BaseModel):
    department: str
    course_number: int
    professor_first: str
    professor_last: str
    professor_email: str

class ClassIdResponse(BaseModel):
    class_id: int

class ClassOut(BaseModel):
    id: int
    course_id: int
    professor_id: int

@router.get("/", response_model=List[ClassOut])
def get_all_classes():
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, course_id, professor_id
                FROM classes
                """
            )
        ).fetchall()
        return [ClassOut(id=row.id, course_id=row.course_id, professor_id=row.professor_id) for row in rows]

@router.get("/{class_id}", response_model=ClassOut)
def get_class_by_id(class_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, course_id, professor_id
                FROM classes
                WHERE id = :class_id
                """
            ),
            {"class_id": class_id}
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail="Class not found")
        return ClassOut(id=row.id, course_id=row.course_id, professor_id=row.professor_id)
    
#attempts to find a class with the given attributes, otherwise it creates one
@router.post("/", response_model=ClassIdResponse)
def create_class(class_request: Class):
    try:
        course_id = create_course(Course(department=class_request.department, number=class_request.course_number))
        prof_id = create_professor(Professor(first=class_request.professor_first, last=class_request.professor_last, email=class_request.professor_email))
    except ValidationError as e:
        errors = [
            {
                "loc":err["loc"],
                "msg":err["msg"],
                "type":err["type"]
            }
            for err in e.errors()
        ]
        raise HTTPException(status_code=422, detail=errors)

    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM classes
                WHERE course_id = :course_id AND professor_id = :professor_id
                """
            ),
            {"course_id": course_id.course_id, "professor_id": prof_id.prof_id},
        ).scalar_one_or_none()

        if ret_id is not None:
            return ClassIdResponse(class_id=ret_id)

        ret_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO classes (course_id, professor_id)
                VALUES (:course_id, :professor_id)
                RETURNING id
                """
            ),
            {"course_id": course_id.course_id, "professor_id": prof_id.prof_id},
        ).scalar_one()
    
    return ClassIdResponse(class_id=ret_id)