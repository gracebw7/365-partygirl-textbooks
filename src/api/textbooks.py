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
    id: int
    title: str
    author: str
    edition: str

@router.get("/test-db-connection")
def test_db_connection():
    # Attempt to connect to the database
    with db.engine.connect() as connection:
        # Execute the query
        result = connection.execute(sqlalchemy.text("SELECT 1")).scalar()
        return {"status": "success", "result": result}

@router.get("/")
def get_textbooks():
    return {"message": "textbooks returned successfully."}

@router.get("/textbooks/{textBookId}")
def get_textbook_by_id(textBookId: int):
    with db.engine.connect() as connection:
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