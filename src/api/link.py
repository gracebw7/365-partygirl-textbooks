from fastapi import APIRouter, Depends, status, HTTPException
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
def create_link(link:Link):
    with db.engine.begin() as connection:
        # Check if the textbook exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id FROM textbooks WHERE id = :textbook_id
                """
            ),
            {"textbook_id": link.textbook_id}
        ).fetchone()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Textbook with id {link.textbook_id} not found."
            )
        
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO links (textbook_id, url)
                VALUES (:textbook_id, :url)
                RETURNING id
                """
            ),
            {"textbook_id": link.textbook_id, "url": link.url},
        ).scalar_one()

    return LinkIdResponse(link_id=ret_id)

@router.post("/{link_id}")
def request_deletion(link_id: int, description: str):
    
    with db.engine.begin() as connection:
        # Check if the link exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id FROM links WHERE id = :link_id
                """), 
                {"link_id": link_id}
            ).fetchone()
        if result is None:
            return {"message": f"Link with id {link_id} not found."}
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO delete_link_requests (link_id, description) 
                VALUES (:link_id, :description) 
                RETURNING id
                """), 
                {"link_id": link_id, "description": description}
            ).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create deletion request for link {link_id}."
            )
        return {"message": f"Deletion request for link {link_id} created successfully.", "request_id": result.id}
    
@router.delete("/{link_id}")
def delete_link(link_id: int):
    with db.engine.begin() as connection:
        # Check if the link exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id FROM links WHERE id = :link_id
                """
            ),
            {"link_id": link_id}
        ).fetchone()
        
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Link with id {link_id} not found."
            )
        
        # Delete the link
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM links WHERE id = :link_id
                """
            ),
            {"link_id": link_id}
        )
        
        return {"message": f"Link with id {link_id} deleted successfully."}



