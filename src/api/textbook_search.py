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

@router.get("/search", response_model=List[Textbook]|None)
def get_search_textbook(department: str = None, 
                         number: int = None, 
                         professorFirst: str = None, 
                         professorLast: str = None,
                         title: str = None, 
                         author: str = None,
                         edition: str = None):
    
    stmt = (
        sqlalchemy.select(
            db.courses.c.department,
            db.courses.c.number,
            db.professors.c.professorFirst,
            db.professors.c.professorLast,
            db.textbooks.c.title,
            db.textbooks.c.author,
            db.textbooks.c.edition,
        )
        .select_from(
            db.classes
            .join(db.courses, db.classes.c.course_id == db.courses.c.id)
            .join(db.professors, db.classes.c.professor_id == db.professors.c.id)
            .join(db.textbook_classes, db.textbook_classes.c.class_id == db.classes.c.id)
            .join(db.textbooks, db.textbooks.c.id == db.textbook_classes.c.textbook_id)
        )
        .limit(10)
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        tbooks = []
        for row in result:
            tbooks.append(
                {
                    "movie_id": row.movie_id,
                    "movie_title": row.title,
                    "year": row.year,
                    "imdb_rating": row.imdb_rating,
                    "imdb_votes": row.imdb_votes,
                }
            )

    return tbooks

@router.get("/search_by_prof", response_model=Textbook|None)
def search_textbook_by_prof(
    department: str, 
    number: int, 
    professorFirst: str, 
    professorLast: str
    ):
    
    class_id = create_get_class(Class(department=department, number=number, prof_first=professorFirst, prof_last=professorLast)).class_id
    print(f"{class_id}")

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

        rows = t_ids.all()   
        print(f"{rows}")
        if not rows:
            return None

        t_list = []

        for t_id in rows:
            links = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT l.url
                    FROM links AS l
                    WHERE l.textbook_id = :id
                    """
                ), [{"id": t_id.id}]
            ).scalars()

            urls = [url for url in links]
            
            t_list.append(
                Textbook(
                    id=t_id.id, 
                    title=t_id.title, 
                    author=t_id.author, 
                    edition=t_id.edition, 
                    links=urls
                    ))

        return t_list


@router.get("/search_by_title", response_model=Textbook|None)
def search_textbook_by_title(title: str, 
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
                    WHERE l.textbook_id = :id
                    """
                ), [{"id": ret_id}]
            ).scalars()
            
        return Textbook(
                    id=ret_id, 
                    title=title, 
                    author=author, 
                    edition=edition, 
                    links=links
                    )
