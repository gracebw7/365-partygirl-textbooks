from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth, professors, classes, courses, classbooks, link as links
from src import database as db


router = APIRouter(
    prefix="/textbooks",
    tags=["textbooks"],
    dependencies=[Depends(auth.get_api_key)],
)

class Textbook(BaseModel):
    title: str
    author: str
    edition: str
    

@router.get("/test-db-connection")
def test_db_connection():
    # Attempt to connect to the database
    with db.engine.begin() as connection:
        # Execute the query
        result = connection.execute(sqlalchemy.text("SELECT 1")).scalar()
        return {"status": "success", "result": result}


@router.get("/", response_model=list[Textbook])
def get_textbooks():
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    *
                FROM 
                    textbooks 
                """
            ) 
            ).fetchall()
    return [Textbook(title=row.title, author=row.author, edition=row.edition) for row in result]

class TextbookInputResponse(BaseModel):
    textbook_id: int
    professor_id: int
    course_id: int
    class_id: int
    classbook_id: int
    link_id: int

class TextbookInput(BaseModel):
    title: str
    author: str
    edition: str
    prof_first: str
    prof_last: str
    department: str
    course_number: int
    url: str

@router.post("/all_info", response_model=TextbookInputResponse)
def add_textbook_info(input: TextbookInput):
    professor = professors.create_get_professor(professors.Professor(first=input.prof_first, last=input.prof_last))
    course = courses.create_get_course(courses.Course(department=input.department, number=input.course_number))
    class_ = classes.create_get_class(classes.Class(department=input.department, number=input.course_number, prof_first=input.prof_first, prof_last=input.prof_last))
    textbook = create_get_textbook(Textbook(title=input.title, author=input.author, edition=input.edition))
    classbook = classbooks.create_classbook(class_id=class_.class_id, book_id=textbook.textbook_id)
    link = links.create_link(textbook_id=textbook.textbook_id, url=input.url)

    return TextbookInputResponse(
        textbook_id=textbook.textbook_id,
        professor_id=professor.prof_id,
        course_id=course.course_id,
        class_id=class_.class_id,
        classbook_id=classbook.classbook_id,
        link_id=link.link_id
    )


@router.get("/textbooks/{textBookId}", response_model=Textbook)
def get_textbook_by_id(textBookId: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT 
                    id, title, author, edition 
                FROM 
                    textbooks 
                WHERE 
                    id = :id
                """), 
                {"id": textBookId}
            ).fetchone()
        if result is None:
            return {"message": f"textbook with id {textBookId} not found."}
        return Textbook(
            id=result.id,
            title=result.title,
            author=result.author,
            edition=result.edition
        )
    
class TextbookIdResponse(BaseModel):
    textbook_id: int

'''
class TextbookCreateResponse(BaseModel):
    textbook_id: int

@router.post("/", response_model=TextbookCreateResponse)
def create_textbook(title: str, author: str, edition: str):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO textbooks (title, author, edition) 
                VALUES (:title, :author, :edition) 
                RETURNING id
                """), 
                {"title": title, "author": author, "edition": edition}
            ).fetchone()
        return TextbookCreateResponse(textbook_id=result.id)
'''

#attempts to find a textbook with the given attributes, otherwise it creates one
@router.post("/", response_model=TextbookIdResponse)
def create_get_textbook(text_request:Textbook):

    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM textbooks
                WHERE title = :title AND author = :author AND edition = :edition
                """
            ),
            {"title":text_request.title,"author":text_request.author,"edition":text_request.edition},
        ).scalar_one_or_none()

        if ret_id is not None:
            return TextbookIdResponse(textbook_id=ret_id)

    with db.engine.begin() as connection:
        ret_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO textbooks (title, author, edition)
                    VALUES (:title, :author, :edition)
                    RETURNING id
                    """
                ),
                {"title":text_request.title,"author":text_request.author,"edition":text_request.edition},
            ).scalar_one()
    
    return TextbookIdResponse(textbook_id=ret_id)




class TextbookLinks(BaseModel):
    links: list[str]

#returns the link relating to a textbook
@router.get("/{textBookId}/links", response_model=list[str])
def get_textbook_links(textBookId: int):

    #NOTE: add error checking if id dne

    with db.engine.begin() as connection:
        links = connection.execute(
            sqlalchemy.text(
                """
                SELECT url
                FROM links
                WHERE textbook_id = :id
                """
            ),
            {"id":textBookId},
        ).scalars().all()

    if not links:
        return []

    return links