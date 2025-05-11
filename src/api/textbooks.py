from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
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

@router.get("/")
def get_textbooks():
    return {"message": "textbooks returned successfully."}

@router.get("/textbooks/{textBookId}")
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
    text_id: int

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
            return TextbookIdResponse(text_id = ret_id)

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
    
    return TextbookIdResponse(text_id = ret_id)


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