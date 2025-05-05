from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import update
from src.api.classes import Class, create_get_class

router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[Depends(auth.get_api_key)],
)

class Textbook(BaseModel):
    id: int
    title: str
    author: str
    edition: str
    link: List[str]

@router.get("/search", response_model=Textbook)
def post_search_textbook_prof(department: str, 
                         number: int, 
                         professorFirst: str, 
                         professorLast: str,
                         title: str, 
                         author: str,
                         edition: str):
    
    class_id = create_get_class(Class(department=department, number=number, prof_first=professorFirst, prof_last=professorLast))
    
    with db.engine.begin() as connection:
        t_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT t.Id, t.title, t.author, t.edition
                FROM textbooks AS t
                JOIN textbook-classes AS tc ON t.id = tc.textbookId
                WHERE tc.classId = :class_id
                """
            ), [{"class_id": class_id}]
        )

        t_list = []

        for t_id in t_ids:
            links = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT l.url
                    FROM links AS l
                    JOIN textbooks AS t ON l.textbookId = :id
                    """
                ), [{"id": t_id.Id}]
            ).scalars()

            t_list.append(Textbook(id=t_id.Id, title=t_id.title, author=t_id.author, edition=t_id.edition, links=links))

        return t_list
 