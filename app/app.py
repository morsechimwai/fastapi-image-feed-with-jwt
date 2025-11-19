# Standard library imports
import shutil
import os
import uuid
import tempfile

# Third-party imports
from sqlalchemy import select
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from datetime import datetime
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


# Lifespan to create the database and tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield # Yield to the main app

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):

    temp_file_path = None


    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200:

            post = Post(
                caption=caption,
                url=upload_result.url,
                file_id=upload_result.file_id,  # Store file_id for deletion
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    # Convert the posts to a list of dictionaries
    posts_data = []
    for post in posts:
        posts_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": datetime.isoformat(post.created_at)
        })

    return {"posts": posts_data}

@app.delete("/post/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Delete the file from ImageKit using file_id
        try:
            if post.file_id:
                delete_result = imagekit.delete_file(post.file_id)
                print(f"File deleted from ImageKit: {post.file_id}")
            else:
                print(f"Warning: No file_id found for post {post.id}, skipping ImageKit deletion")
        except Exception as delete_error:
            print(f"Error deleting file from ImageKit: {delete_error}")
            # Continue with database deletion even if ImageKit deletion fails

        # Delete the post from the database
        await session.delete(post)
        await session.commit()
        print(f"Post deleted from database: {post.id}")
        return {"success": True, "message": "Post deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
