
from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    dependencies=[Depends(auth.get_api_key)],
)

class Course(BaseModel):
    department: str
    number: int

class CourseIdResponse(BaseModel):
    course_id: int

#attempts to find a course with the given attributes, otherwise it creates one
@router.post("/", response_model=CourseIdResponse)
def create_get_course(course_request:Course):

    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM courses
                WHERE department = :department AND number = :number
                """
            ),
            {"department": course_request.department, "number": course_request.number},
        ).scalar_one_or_none()

        if ret_id is not None:
            return CourseIdResponse(course_id = ret_id)

    with db.engine.begin() as connection:
        ret_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO courses (department, number)
                    VALUES (:department, :number)
                    RETURNING id
                    """
                ),
                {"department": course_request.department, "number": course_request.number},
            ).scalar_one()
    
    return CourseIdResponse(course_id = ret_id)