"""API dependencies."""
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.db.models import User
from app.users.manager import current_active_user


async def get_db() -> AsyncSession:
    """Get database session dependency."""
    async for session in get_async_session():
        yield session


async def get_current_user() -> User:
    """Get current authenticated user dependency."""
    return await current_active_user()

