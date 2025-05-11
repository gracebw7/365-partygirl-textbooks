from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/links",
    tags=["links"],
    dependencies=[Depends(auth.get_api_key)],
)

class Link(BaseModel):
    textbook_id: int
    url: str

class LinkIdResponse(BaseModel):
    link_id: int



@router.post("/", response_model=LinkIdResponse)
def create_link(textbook_id: int, url: str):
    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO links (textbook_id, url)
                VALUES (:textbook_id, :url)
                RETURNING id
                """
            ),
            {"textbook_id": textbook_id, "url": url},
        ).scalar_one()

    return LinkIdResponse(link_id=ret_id)



