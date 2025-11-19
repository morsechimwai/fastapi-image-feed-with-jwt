"""API v1 package."""
from fastapi import APIRouter
from app.api.v1 import auth, users, posts
from app.api.v1.posts import upload_file, get_feed, delete_post

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, tags=["posts"])

# Backward compatibility: Keep old endpoints without /posts prefix
api_router.add_api_route("/upload", upload_file, methods=["POST"], tags=["posts"])
api_router.add_api_route("/feed", get_feed, methods=["GET"], tags=["posts"])
api_router.add_api_route("/post/{post_id}", delete_post, methods=["DELETE"], tags=["posts"])

__all__ = ["api_router"]

