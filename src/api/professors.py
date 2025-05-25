from dataclasses import dataclass
from fastapi import APIRouter, Depends, status
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
