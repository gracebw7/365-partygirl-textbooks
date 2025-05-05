from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import update

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
    links: str

@router.get("/search", response_model=Textbook)
def post_search_textbook(department: str, 
                         courseId: int, 
                         professorId: int, 
                         title: str, 
                         author: str,
                         edition: str):
    
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT t.Id, t.title, t.author, t.edition, l.url
                FROM textbooks AS t
                JOIN links AS l ON t.id = l.textbook_id
                WHERE EXISTS (
                    SELECT 1
                    FROM textbook-classes AS tc
                    JOIN classes AS c ON c.id = tc.class_id
                    WHERE tc.textbook_id = t.id AND c.professor_id = :professorId AND c.course_id = :courseId 
                )
                """
            ),
            [{"professorId": professorId,
            "courseId": courseId}],
        )     

        t=Textbook(id=row.Id, title=row.title, author=row.author, edition=row.edition, links=row.url)

        print(t)

        return t
 