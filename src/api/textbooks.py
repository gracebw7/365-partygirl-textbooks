from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth, professors, classes, courses, classbooks, link as links
from src import database as db
from src.api.link import Link


router = APIRouter(
    prefix="/textbooks",
    tags=["textbooks"],
    dependencies=[Depends(auth.get_api_key)],
)

class Textbook(BaseModel):
    title: str
    author: str
    edition: str


class TextbookIdResponse(BaseModel):
    textbook_id: int

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

@router.get("/{textBookId}", response_model=Textbook)
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
            raise HTTPException(
                status_code=404,
                detail=f"Textbook with id {textBookId} not found."
            )
        return Textbook(
            id=result.id,
            title=result.title,
            author=result.author,
            edition=result.edition
        )
    

@router.post("/", response_model=TextbookIdResponse)
def create_textbook(textbook: Textbook):
    with db.engine.begin() as connection:
        # Check if the textbook already exists
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM textbooks
                WHERE title = :title AND author = :author AND edition = :edition
                """
            ),
            {"title": textbook.title, "author": textbook.author, "edition": textbook.edition},
        ).scalar_one_or_none()

        if ret_id is not None:
            return TextbookIdResponse(textbook_id=ret_id)

        # Create a new textbook if it doesn't exist
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO textbooks (title, author, edition)
                VALUES (:title, :author, :edition)
                RETURNING id
                """
            ),
            {"title": textbook.title, "author": textbook.author, "edition": textbook.edition},
        ).scalar_one()

    return TextbookIdResponse(textbook_id=ret_id)

@router.get("/{textBookId}/links", response_model=list[str])
def get_textbook_links(textBookId: int):
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