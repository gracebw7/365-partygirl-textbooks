from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

from src.api.classes import Class, create_get_class
from src.api.textbooks import Textbook, create_get_textbook, get_textbook_links, get_textbook_by_id

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

@router.post("/", response_model=List[Textbook])
def find_by_schedule(schedule: List[Class]):
    results = []

    for item in schedule: 
        class_id = create_get_class(Class(department=item.department,number=item.number,prof_first=item.prof_first,prof_last=item.prof_last)).class_id

    with db.engine.begin() as connection:
        text_ids = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT textbook_id
                    FROM "textbook-classes"
                    JOIN textbooks ON textbook_id = textbooks.id
                    WHERE class_id = :class_id
                    """
                ),
                {"class_id": class_id},
            ).scalars().all()
        
    for id in text_ids:
        textbook = get_textbook_by_id(id)
        links = get_textbook_links(id)
        results.append(TextbookReturn(title=textbook.title,author=textbook.author,edition=textbook.edition,links=links))
    
    return results
    