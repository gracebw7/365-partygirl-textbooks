from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api import textbooks, courses, professors, classes

description = """
Central Coast Cauldrons is the premier ecommerce site for all your alchemical desires.
"""
tags_metadata = [
    {"name": "textbooks", "description": "textbook transactions."},
]

app = FastAPI(
    title="365-partygirl-textbooks",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "PartyGirls",
        "email": "tbd@gmail.com",
    },
    openapi_tags=tags_metadata,
)

origins = ["https://365partygirl-books.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers for different parts of the API (endpoints)
app.include_router(textbooks.router)
app.include_router(courses.router)
app.include_router(professors.router)
app.include_router(classes.router)



@app.get("/")
async def root():
    return {"message": "Shop is open for business!"}
