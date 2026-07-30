from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.auth import router as auth_router
from app.api.locations import router as locations_router
from app.api.operators import router as operators_router
from app.api.buses import router as buses_router
from app.database.session import engine


app = FastAPI(
    title="Bus Marketplace API",
    version="1.0.0",
    description=(
        "Backend APIs for authentication, locations, operators, "
        "and fleet management."
    ),
)

app.include_router(auth_router)
app.include_router(locations_router)
app.include_router(operators_router)
app.include_router(buses_router)


@app.get("/", tags=["System"])
def root():
    return {
        "application": "Bus Marketplace API",
        "message": "Welcome to Bus Marketplace API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


@app.get("/health", tags=["System"])
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable.",
        ) from exc