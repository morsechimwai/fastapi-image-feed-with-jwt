"""Database initialization."""
from app.db.base import Base
from app.db.session import engine


async def create_db_and_tables():
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

