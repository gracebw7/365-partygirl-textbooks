from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, HttpUrl
import sqlalchemy
from src.api import auth
from src import database as db
from typing import List

router = APIRouter(
    prefix="/links",
    tags=["links"],
    dependencies=[Depends(auth.get_api_key)],
)

class Link(BaseModel):
    textbook_id: int
    url: HttpUrl

class LinkIdResponse(BaseModel):
    link_id: int

class DeleteLinkRequest(BaseModel):
    link_id: int
    description: str = Field(..., max_length=500, description="Reason for deletion request")

class LinkOut(BaseModel):
    id: int
    textbook_id: int
    url: HttpUrl

@router.get("/", response_model=List[LinkOut])
def get_all_links():
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, textbook_id, url
                FROM links
                """
            )
        ).fetchall()
        return [LinkOut(id=row.id, textbook_id=row.textbook_id, url=row.url) for row in rows]

@router.get("/{link_id}", response_model=LinkOut)
def get_link_by_id(link_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, textbook_id, url
                FROM links
                WHERE id = :link_id
                """
            ),
            {"link_id": link_id}
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail=f"Link with id {link_id} not found.")
        return LinkOut(id=row.id, textbook_id=row.textbook_id, url=row.url)
    
@router.post("/", response_model=LinkIdResponse)
def create_link(link:Link):
    try:
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

@router.post("/{link_id}")
def request_deletion(link_req: DeleteLinkRequest):
    with db.engine.begin() as connection:
        # Check if the link exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id FROM links WHERE id = :link_id
                """), 
                {"link_id": link_req.link_id}
            ).fetchone()
        if result is None:
            return {"message": f"Link with id {link_req.link_id} not found."}
        result = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO delete_link_requests (link_id, description) 
                VALUES (:link_id, :description) 
                RETURNING id
                """), 
                {"link_id": link_req.link_id, "description": link_req.description}
            ).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create deletion request for link {link_req.link_id}."
            )
        return {"message": f"Deletion request for link {link_req.link_id} created successfully.", "request_id": result.id}
    
@router.delete("/{link_id}")
def delete_link(link_id: int):
    with db.engine.begin() as connection:
        # Check if the link exists
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id for update FROM links WHERE id = :link_id
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



