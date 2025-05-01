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