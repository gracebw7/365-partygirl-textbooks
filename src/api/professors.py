from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(
    prefix="/professors",
    tags=["professors"],
    dependencies=[Depends(auth.get_api_key)],
)

class Professor(BaseModel):
    first: str
    last: str

class ProfessorIdResponse(BaseModel):
    prof_id: int

class ProfessorOut(BaseModel):
    id: int
    first: str
    last: str

@router.get("/", response_model=List[ProfessorOut])
def get_all_professors():
    with db.engine.begin() as connection:
        rows = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, first, last
                FROM professors
                """
            )
        ).fetchall()
        return [ProfessorOut(id=row.id, first=row.first, last=row.last) for row in rows]

@router.get("/{professor_id}", response_model=ProfessorOut)
def get_professor_by_id(professor_id: int):
    with db.engine.begin() as connection:
        row = connection.execute(
            sqlalchemy.text(
                """
                SELECT id, first, last
                FROM professors
                WHERE id = :professor_id
                """
            ),
            {"professor_id": professor_id}
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail="Professor not found")
        return ProfessorOut(id=row.id, first=row.first, last=row.last)
    
@router.post("/", response_model=ProfessorIdResponse)
def create_professor(prof_request:Professor):
    with db.engine.begin() as connection:
        ret_id = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM professors
                WHERE first = :first AND last = :last
                """
            ),
            {"first":prof_request.first, "last": prof_request.last},
        ).scalar_one_or_none()

        if ret_id is not None:
            return ProfessorIdResponse(prof_id = ret_id)

        ret_id = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO professors (first, last)
                    VALUES (:first, :last)
                    RETURNING id
                    """
                ),
                {"first":prof_request.first, "last": prof_request.last},
            ).scalar_one()
    
    return ProfessorIdResponse(prof_id = ret_id)
