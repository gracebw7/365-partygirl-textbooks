from dataclasses import dataclass
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List

import sqlalchemy
from src.api import auth
from src import database as db

from faker import Faker

import random 

faker = Faker()


def make_fake_textbook():
        author = f"{faker.firtst_name()} {faker.last_name()}"

        title_words = [faker.word().capitalize() for i in range(random.randint(2,5))]
        title = " ".join(title_words)

        edition = random.randint(1,10)

        links = [faker.url() for i in range (10)]

        return (author, title, edition, links)



with db.engine.begin() as connection:
        
        row = connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO textbooks (title, author, edition)
                SELECT , department, number
                FROM courses
                WHERE id = :course_id
                """
            ),
            {"course_id": course_id}
        ).first()
