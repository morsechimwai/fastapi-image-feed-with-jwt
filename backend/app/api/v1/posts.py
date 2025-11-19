"""Posts API endpoints."""
import os
import shutil
import tempfile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Depends
from app.db.models import User, Post
from app.db.session import get_async_session
from app.users.manager import current_active_user
from app.services.imagekit import imagekit
from app.schemas.post import PostInFeed
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Upload an image or video file."""
    temp_file_path = None

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        # Upload to ImageKit
        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200:
            # Create post in database
            post = Post(
                user_id=str(user.id),
                caption=caption,
                url=upload_result.url,
                file_id=upload_result.file_id,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        else:
            raise HTTPException(status_code=500, detail="Failed to upload file to ImageKit")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.get("/feed", response_model=dict)
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Get all posts in the feed."""
    # Get all posts ordered by creation date
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()

    # Get all users to map user_id to email
    user_result = await session.execute(select(User))
    users = user_result.scalars().all()
    user_dict = {str(user.id): user.email for user in users}

    # Convert posts to feed format
    posts_data = []
    for post in posts:
        posts_data.append(
            PostInFeed(
                id=str(post.id),
                user_id=str(post.user_id),
                caption=post.caption,
                url=post.url,
                file_type=post.file_type,
                file_name=post.file_name,
                file_id=post.file_id,
                created_at=post.created_at,
                is_owner=str(post.user_id) == str(user.id),
                email=user_dict.get(str(post.user_id), "Unknown"),
            ).model_dump()
        )

    return {"posts": posts_data}


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Delete a post."""
    # Get post from database
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check authorization
    if str(post.user_id) != str(user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    # Delete file from ImageKit
    try:
        if post.file_id:
            imagekit.delete_file(post.file_id)
            print(f"File deleted from ImageKit: {post.file_id}")
    except Exception as delete_error:
        print(f"Error deleting file from ImageKit: {delete_error}")
        # Continue with database deletion even if ImageKit deletion fails

    # Delete post from database
    await session.delete(post)
    await session.commit()

    return {"success": True, "message": "Post deleted successfully"}

