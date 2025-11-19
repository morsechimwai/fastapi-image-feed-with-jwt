"""FastAPI application main file."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.init_db import create_db_and_tables
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Create database tables
    await create_db_and_tables()
    yield
    # Shutdown: Cleanup if needed


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

# Include API routers (new structure)
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs"
    }

