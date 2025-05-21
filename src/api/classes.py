
from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

from src.api.courses import Course, create_get_course
from src.api.professors import Professor, create_get_professor

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Class(BaseModel):
    department: str
    number: int
    prof_first: str
    prof_last: str

class ClassIdResponse(BaseModel):
    class_id: int

#attempts to find a class with the given attributes, otherwise it creates one
@router.post("/", response_model=ClassIdResponse)
def create_get_class(class_request:Class):
    course_id = create_get_course(Course(department=class_request.department,number=class_request.number))
    prof_id = create_get_professor(Professor(first=class_request.prof_first,last=class_request.prof_last))

    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM classes
                WHERE course_id = :course_id AND professor_id = :professor_id
                """
            ),
            {"course_id":course_id.course_id, "professor_id": prof_id.prof_id},
        ).scalar_one_or_none()

        if ret_id is not None:
            return ClassIdResponse(class_id = ret_id)

        ret_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO classes (course_id, professor_id)
                    VALUES (:course_id, :professor_id)
                    RETURNING id
                    """
                ),
                {"course_id":course_id.course_id, "professor_id": prof_id.prof_id},
            ).scalar_one()
    
    return ClassIdResponse(class_id = ret_id)