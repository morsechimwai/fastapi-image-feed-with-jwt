"""Database session management."""
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

# Create the engine and session maker
engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get an async database session."""
    async with async_session_maker() as session:
        yield session

