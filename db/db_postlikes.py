from fastapi.responses import JSONResponse
from sqlalchemy import JSON, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db.models import DbPost, DbUser, DbPostLike


# Functions to handle post likes CRUD operations
def create_like(db: Session, post_id: int, user_id: int):
    # Check if post exists
    post = db.query(DbPost).filter(DbPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )

    # Check if user exists
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    # Prevent users from liking their own posts
    if post.user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot like your own post",
        )

    # Check if user has already liked this post
    existing_like = (
        db.query(DbPostLike)
        .filter(DbPostLike.post_id == post_id, DbPostLike.user_id == user_id)
        .first()
    )

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post",
        )

    # Create new like
    new_like = DbPostLike(post_id=post_id, user_id=user_id)

    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


def delete_like(db: Session, post_id: int, user_id: int):
    # Find the like
    like = (
        db.query(DbPostLike)
        .filter(DbPostLike.post_id == post_id, DbPostLike.user_id == user_id)
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't liked this post yet",
        )

    db.delete(like)
    db.commit()
    return JSONResponse(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
    )


def get_post_likes_count(db: Session, post_id: int):
    return db.query(DbPostLike).filter(DbPostLike.post_id == post_id).count()


def has_user_liked_post(db: Session, post_id: int, user_id: int):
    return (
        db.query(DbPostLike)
        .filter(DbPostLike.post_id == post_id, DbPostLike.user_id == user_id)
        .first()
        is not None
    )
