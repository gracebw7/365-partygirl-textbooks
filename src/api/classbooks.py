from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/classbooks",
    tags=["classbooks"],
    dependencies=[Depends(auth.get_api_key)],
)

class Classbook(BaseModel):
    id: int
    book_id: str
    class_id: int


class ClassBookIdResponse(BaseModel):
    classbook_id: int

@router.post("/", response_model=ClassBookIdResponse)
def create_classbook(class_id: int, book_id: str):
    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO "textbook-classes" (class_id, textbook_id)
                VALUES (:class_id, :book_id)
                RETURNING id
                """
            ),
            {"class_id": class_id, "book_id": book_id},
        ).scalar_one()

    return ClassBookIdResponse(classbook_id=ret_id)

