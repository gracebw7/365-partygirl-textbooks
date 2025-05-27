
from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
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
    department: str = Field(..., min_length=2, max_length=4)
    number: int = Field(..., ge=100, le=999)

    @field_validator('department')
    @classmethod
    def department_must_be_all_caps(cls,v):
        if not v.isupper():
            raise ValueError('Department must be all uppercase')
        return v

class CourseIdResponse(BaseModel):
    course_id: int

class CourseOut(BaseModel):
    id: int
    department: str
    number: int

@router.get("/", response_model=List[CourseOut])
def get_all_courses():
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, department, number
                FROM courses
                """
            )
        ).fetchall()
        return [CourseOut(id=row.id, department=row.department, number=row.number) for row in rows]

@router.get("/{course_id}", response_model=CourseOut)
def get_course_by_id(course_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, department, number
                FROM courses
                WHERE id = :course_id
                """
            ),
            {"course_id": course_id}
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseOut(id=row.id, department=row.department, number=row.number)

@router.post("/", response_model=CourseIdResponse)
def create_course(course_request:Course):
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