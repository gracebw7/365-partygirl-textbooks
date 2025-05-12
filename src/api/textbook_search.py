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
    links: List[str]

@router.get("/search_by_prof", response_model=Textbook|None)
def post_search_textbook_prof(department: str, 
                         number: int, 
                         professorFirst: str, 
                         professorLast: str):
    
    class_id = create_get_class(Class(department=department, number=number, prof_first=professorFirst, prof_last=professorLast)).class_id
    
    with db.engine.begin() as connection:
        t_ids = connection.execute(
            sqlalchemy.text(
                """
                SELECT t.id, t.title, t.author, t.edition
                FROM textbooks AS t
                JOIN textbook_classes AS tc ON t.id = tc.textbook_id
                WHERE tc.class_id = :class_id
                """
            ), [{"class_id": class_id}]
        )

        if t_ids.scalar_one_or_none() is None:
            return None

        t_list = []

        for t_id in t_ids:
            links = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT l.url
                    FROM links AS l
                    JOIN textbooks AS t ON l.textbook_id = :id
                    """
                ), [{"id": t_id.id}]
            ).scalars()
            
            t_list.append(Textbook(id=t_id.id, 
                                   title=t_id.title, 
                                   author=t_id.author, 
                                   edition=t_id.edition, 
                                   links=links))

        return t_list[0]


@router.get("/search_by_title", response_model=Textbook|None)
def post_search_textbook_prof(title: str, 
                            author: str,
                            edition: str):
        
    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM textbooks
                WHERE title = :title AND author = :author AND edition = :edition
                """
            ),
            {"title":title,"author":author,"edition":edition},
        ).scalar_one_or_none()

        if ret_id is None:
            return None

        links = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT l.url
                    FROM links AS l
                    JOIN textbooks AS t ON l.textbook_id = :id
                    """
                ), [{"id": ret_id}]
            ).scalars()
            
        return Textbook(id=ret_id, 
                        title=title, 
                        author=author, 
                        edition=edition, 
                        links=links)
