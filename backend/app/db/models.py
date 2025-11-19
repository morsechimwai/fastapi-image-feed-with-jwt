"""Database models."""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model."""
    __tablename__ = "user"

    # Relationships
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    """Post model for images and videos."""
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    caption = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    file_id = Column(String, nullable=True)  # ImageKit file ID for deletion
    file_type = Column(String, nullable=False)  # 'image' or 'video'
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    # Relationships
    user = relationship("User", back_populates="posts")

