# crud.py
from sqlalchemy.orm.session import Session
from db.models import DbPost, DbUser, DbPostLike
from schemas import PostBase, PostDisplay, PostUpdate
from fastapi import HTTPException, Response, status
import datetime
from typing import List, Optional
from db.db_postlikes import get_post_likes_count, has_user_liked_post


def create_post(db: Session, request: PostBase):
    new_post = DbPost(
        content=request.content,
        user_id=request.user_id,
        username=request.username,
        timestamp=datetime.datetime.now(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session, current_user_id: Optional[int] = None) -> List[PostDisplay]:
    posts = db.query(DbPost).all()

    # Convert to PostDisplay with likes info
    result = []
    for post in posts:
        likes_count = get_post_likes_count(db, post.id)
        liked_by_user = False
        if current_user_id:
            liked_by_user = has_user_liked_post(db, post.id, current_user_id)

        post_dict = {
            "id": post.id,
            "content": post.content,
            "user": post.user,
            "user_id": post.user_id,
            "images": post.images,
            "timestamp": post.timestamp,
            "likes_count": likes_count,
            "liked_by_user": liked_by_user,
        }

        result.append(PostDisplay(**post_dict))

    return result


def get_post(db: Session, id: int, current_user_id: Optional[int] = None):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )  # stop the code running

    # Get likes info
    likes_count = get_post_likes_count(db, post.id)
    liked_by_user = False
    if current_user_id:
        liked_by_user = has_user_liked_post(db, post.id, current_user_id)

    # Add the likes info to the post
    post_dict = {
        "id": post.id,
        "content": post.content,
        "user": post.user,
        "user_id": post.user_id,
        "images": post.images,
        "timestamp": post.timestamp,
        "likes_count": likes_count,
        "liked_by_user": liked_by_user,
    }

    return PostDisplay(**post_dict)


def update_post(
    db: Session, id: int, request: PostUpdate
):  # Update post function now accepts PostUpdate model
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    # Update the post content and image_url if provided
    post.content = request.content
    post.image_url = request.image_url

    db.commit()
    return post


def delete_post(db: Session, id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    db.delete(post)
    db.commit()
    return Response(status_code=204)
