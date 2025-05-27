from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from sqlalchemy import bindparam
from src.api import auth
from src import database as db

from src.api.classes import Class, create_class
from src.api.textbooks import Textbook, get_textbook_links, get_textbook_by_id

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
    dependencies=[Depends(auth.get_api_key)],
)

class TextbookReturn(BaseModel):
    title: str
    author: str
    edition: str
    links: List[str]

@router.post("/", response_model=List[TextbookReturn])
def find_by_schedule(schedule: List[Class]):
    results = []
    class_ids = []


    with db.engine.begin() as connection:

        # loop through and find all class ids
        for item in schedule: 
            #class_ = Class(department=item.department, number=item.number, prof_first=item.prof_first, prof_last=item.prof_last)
            #class_ids.append(create_class(class_).class_id)

            class_id = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT classes.id
                    FROM classes
                    JOIN professors ON professor_id = professors.id
                    JOIN courses ON course_id = courses.id
                    WHERE department = :department AND number = :number AND first = :professor_first AND last = :professor_last AND email = :professor_email
                    """
                ),
                {"department": item.department, "number": item.course_number, "professor_first": item.professor_first, "professor_last":item.professor_last, "professor_email":item.professor_email}  # Pass as tuple for SQLAlchemy IN clause
            ).scalars().one_or_none()

            if class_id is not None:
                class_ids.append(class_id)

        if class_ids == []:
            raise HTTPException(status_code=404, detail="No matching classes not found")

        # Use a single query to get all textbook_ids for the given class_ids
        text_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT DISTINCT textbook_id
                FROM textbook_classes
                JOIN textbooks ON textbook_id = textbooks.id
                WHERE class_id IN :class_ids
                """
            ).bindparams(bindparam("class_ids", expanding=True)),
            {"class_ids": class_ids}  # Pass as tuple for SQLAlchemy IN clause
        ).scalars().all()

        if text_ids == []:
            raise HTTPException(status_code=404, detail="No matching textbooks not found")
        
    for id in text_ids:
        if id is not None:
            textbook = get_textbook_by_id(id)
            links = get_textbook_links(id)
            new_textbook = TextbookReturn(title=textbook.title, author=textbook.author, edition=textbook.edition, links=links)
            results.append(new_textbook)

    return results
    