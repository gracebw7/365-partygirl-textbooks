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
    try:
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
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Textbooks not found.")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while retrieving textbooks.")

@router.get("/{textBookId}", response_model=Textbook)
def get_textbook_by_id(textBookId: int):
    try:
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
                    """
                ), 
                {"id": textBookId}
            ).fetchone()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Textbook with id {textBookId} not found."
            )
        return Textbook(
            title=result.title,
            author=result.author,
            edition=result.edition
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while retrieving textbook.")

@router.post("/", response_model=TextbookIdResponse)
def create_textbook(textbook: Textbook):
    try:
        with db.engine.begin() as connection:
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
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while creating textbook.")

@router.get("/{textBookId}/links", response_model=list[str])
def get_textbook_links(textBookId: int):
    try:
        with db.engine.begin() as connection:
            links = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT url
                    FROM links
                    WHERE textbook_id = :id
                    """
                ),
                {"id": textBookId},
            ).scalars().all()

        if not links:
            return []

        return links
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while retrieving links.")
