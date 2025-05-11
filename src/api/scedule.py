from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

from src.api.classes import Class, create_get_class
from src.api.textbooks import Textbook, create_get_textbook, get_textbook_links

router = APIRouter(
    prefix="/schedule",
    tags=["scedule"],
    dependencies=[Depends(auth.get_api_key)],
)

class TextbookReturn(BaseModel):
    id: int
    title: str
    author: str
    edition: str
    links: List[str]

@router.post("/", response_model=List[Textbook])
def find_by_schedule(schedule: List[Class]):
    results = []

    for item in schedule: 
        class_id = create_get_class(Class(department=item.department,number=item.number,first=item.prof_first,last=item.prof_last)).class_id

    with db.engine.begin() as connection:
        connection.execute(
                sqlalchemy.text(
                    """
                    SELECT id
                    FROM textbooks-classes
                    JOIN textbooks ON textbook_id = textbooks.id
                    WHERE class_id = class_id
                    """
                ),
                {"title":text_request.title,"author":text_request.author,"edition":text_request.edition},
            ).scalar_one_or_none()