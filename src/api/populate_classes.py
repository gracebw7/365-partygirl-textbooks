import sqlalchemy
from fastapi import APIRouter
from faker import Faker
from src import database as db

import random

router = APIRouter(
    prefix="/debug",
    tags=["debug"],
)


@router.post("/populate_classes")
def generate_data():
    num_profs = 500
    fake = Faker()
    profs_per_course = 10
    num_courses = 1000
    books_per_class = 10
    links_per_book = 10

    with db.engine.begin() as conn:
        print("creating fake classes...")

        for i in range(num_courses):
            if i % 10 == 0:
                print(i)
            department = (
                fake.random_uppercase_letter()
                + fake.random_uppercase_letter()
                + fake.random_uppercase_letter()
            )
            number = fake.random_int(min=100, max=599)
            course_id = conn.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO courses (department, number)
                    VALUES (:department, :number)
                    RETURNING id
                    """
                ),
                {"department": department, "number": number},
            ).scalar_one()
            print("creating professors...")
            for j in range(profs_per_course):
                first = fake.first_name()
                last = fake.last_name()
                email = fake.unique.email()
                prof_id = conn.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO professors (first, last, email)
                        VALUES (:first, :last, :email)
                        RETURNING id
                        """
                    ),
                    {"first": first, "last": last, "email": email},
                ).scalar_one()
                class_id = conn.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO classes (course_id, professor_id)
                        VALUES (:course_id, :professor_id)
                        RETURNING id
                        """
                    ),
                    {"course_id": course_id, "professor_id": prof_id},
                ).scalar_one()
                for k in range(books_per_class):
                    author = f"{fake.first_name()} {fake.last_name()}"

                    title_words = [
                        fake.word().capitalize() for i in range(random.randint(2, 5))
                    ]
                    title = " ".join(title_words)

                    edition = str(random.randint(1, 10))
                    textbook_id = conn.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO textbooks (title, author, edition)
                            VALUES (:title, :author, :edition)
                            RETURNING id
                            """
                        ),
                        {"title": title, "author": author, "edition": edition},
                    ).scalar_one()
                    conn.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO textbook_classes (textbook_id, class_id)
                            VALUES (:textbook_id, :class_id)
                            """
                        ),
                        {"textbook_id": textbook_id, "class_id": class_id},
                    )
                    for l in range(links_per_book):
                        url = fake.unique.url()
                        conn.execute(
                            sqlalchemy.text(
                                """
                                INSERT INTO links (textbook_id, url)
                                VALUES (:textbook_id, :url)
                                """
                            ),
                            {"textbook_id": textbook_id, "url": url},
                        )
        print("done creating fake classes...")
