from fastapi import FastAPI
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.database.session import engine
from app.api.locations import router as locations_router
from app.api.operators import router as operators_router


app = FastAPI(
    title="Bus Marketplace API",
    version="1.0.0",
    description="",
)

app.include_router(auth_router)
app.include_router(locations_router)
app.include_router(operators_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Bus Marketplace API",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "Database Connected Successfully",
    }