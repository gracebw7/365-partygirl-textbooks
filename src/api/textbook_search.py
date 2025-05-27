from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import List
from src.api import auth
from src import database as db
import sqlalchemy
from sqlalchemy import and_, update
from src.api.classes import Class, create_class
from sqlalchemy.sql import true

metadata_obj = sqlalchemy.MetaData()
courses = sqlalchemy.Table("courses", metadata_obj, autoload_with=db.engine)
professors = sqlalchemy.Table("professors", metadata_obj, autoload_with=db.engine)
textbooks = sqlalchemy.Table("textbooks", metadata_obj, autoload_with=db.engine)
textbook_classes = sqlalchemy.Table("textbook_classes", metadata_obj, autoload_with=db.engine)
classes = sqlalchemy.Table("classes", metadata_obj, autoload_with=db.engine)


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

@router.get("/search", response_model=List[Textbook]|str)
def get_search_textbook(department: str = None, 
                         number: int = None, 
                         professorFirst: str = None, 
                         professorLast: str = None,
                         title: str = None, 
                         author: str = None,
                         edition: str = None):
    
    conditions = []

    if department:
        conditions.append(courses.c.department == department)
    if number:
        conditions.append(courses.c.number == number)
    if professorFirst:
        conditions.append(professors.c.first.ilike(f"%{professorFirst}%"))
    if professorLast:
        conditions.append(professors.c.last.ilike(f"%{professorLast}%"))
    if title:
        conditions.append(textbooks.c.title.ilike(f"%{title}%"))
    if author:
        conditions.append(textbooks.c.author.ilike(f"%{author}%"))
    if edition:
        conditions.append(textbooks.c.edition == edition)

    
    stmt = (
        sqlalchemy.select(
            courses.c.department,
            courses.c.number,
            professors.c.first,
            professors.c.last,
            textbooks.c.title,
            textbooks.c.author,
            textbooks.c.edition,
            textbooks.c.id
        )
        .distinct(textbooks.c.id)
        .select_from(
            classes
            .join(courses, classes.c.course_id == courses.c.id)
            .join(professors, classes.c.professor_id == professors.c.id)
            .join(textbook_classes, textbook_classes.c.class_id == classes.c.id)
            .join(textbooks, textbooks.c.id == textbook_classes.c.textbook_id)
        )
        .where(and_(*conditions) if conditions else true())
        .limit(10)
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        tbooks = []
        for row in result:
            links = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT l.url
                    FROM links AS l
                    WHERE l.textbook_id = :id
                    """
                ), [{"id": row.id}]
            ).scalars()

            urls = [url for url in links]
            
            tbooks.append(Textbook(id=row.id, 
                                   title=row.title, 
                                   author=row.author, 
                                   edition=row.edition, 
                                   links=urls))

    if tbooks == []:
        return "No textbooks matching search parameters found. Please adjust your query."
    
    return tbooks

