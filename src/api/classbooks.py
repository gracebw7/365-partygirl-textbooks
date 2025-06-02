from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from sqlalchemy.exc import IntegrityError
from src import database as db

router = APIRouter(
    prefix="/classbooks",
    tags=["classbooks"],
    dependencies=[Depends(auth.get_api_key)],
)


class Classbook(BaseModel):
    book_id: str
    class_id: int


class ClassBookIdResponse(BaseModel):
    classbook_id: int


@router.get("/", response_model=list[Classbook])
def get_all_classbooks():
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, textbook_id AS book_id, class_id
                FROM textbook_classes
                """
            )
        ).fetchall()
        return [
            Classbook(id=row.id, book_id=row.book_id, class_id=row.class_id)
            for row in rows
        ]


@router.get("/{classbook_id}", response_model=Classbook)
def get_classbook_by_id(classbook_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, textbook_id AS book_id, class_id
                FROM textbook_classes
                WHERE id = :classbook_id
                """
            ),
            {"classbook_id": classbook_id},
        ).first()
        if row is None:
            raise HTTPException(
                status_code=404, detail=f"Classbook with id {classbook_id} not found."
            )
        return Classbook(id=row.id, book_id=row.book_id, class_id=row.class_id)


@router.post("/", response_model=ClassBookIdResponse)
def create_classbook(classbook: Classbook):
    class_id = classbook.class_id
    book_id = classbook.book_id
    try:
        with db.engine.begin() as connection:
            # Check if entry already exists
            exists = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT 1 FROM "textbook_classes"
                    WHERE class_id = :class_id AND textbook_id = :book_id
                    """
                ),
                {"class_id": class_id, "book_id": book_id},
            ).first()
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Classbook entry already exists.",
                )

            ret_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO "textbook_classes" (class_id, textbook_id)
                    VALUES (:class_id, :book_id)
                    RETURNING id
                    """
                ),
                {"class_id": class_id, "book_id": book_id},
            ).scalar_one()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert classbook entry due to integrity error.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )

    return ClassBookIdResponse(classbook_id=ret_id)
