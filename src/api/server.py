from fastapi import FastAPI
from src.api import carts, catalog, bottler, barrels, admin, info, inventory
from starlette.middleware.cors import CORSMiddleware

description = """
Central Coast Cauldrons is the premier ecommerce site for all your alchemical desires.
"""
tags_metadata = [
    {"name": "cart", "description": "Place potion orders."},
    {"name": "catalog", "description": "View the available potions."},
    {"name": "bottler", "description": "Bottle potions from the raw magical elixir."},
    {
        "name": "barrels",
        "description": "Buy barrels of raw magical elixir for making potions.",
    },
    {"name": "admin", "description": "Where you reset the game state."},
    {"name": "info", "description": "Get updates on time"},
    {
        "name": "inventory",
        "description": "Get the current inventory of shop and buying capacity.",
    },
]

app = FastAPI(
    title="365-partygirl-textbooks",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "PartyGirls",
        "email": "tbd",
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
#app.include_router(inventory.router)



@app.get("/")
async def root():
    return {"message": "Shop is open for business!"}
