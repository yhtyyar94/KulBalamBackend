from typing import List
from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase, PostDisplay
from db.models import DbPost, DbUser
from fastapi import HTTPException, Response, status
from db.db_postlikes import get_post_likes_count, has_user_liked_post


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_user(db: Session):
    return db.query(DbUser).all()


def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user


def get_username(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if user:
        return user.username
    return None


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user


def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    user.update(
        {
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.password: Hash.bcrypt(request.password),
        }
    )
    db.commit()
    user = db.query(DbUser).filter(DbUser.id == id).first()
    return user


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=204)


def get_product_by_user_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found.",
        )
    return user


def get_posts_by_user_id(
    db: Session, id: int, current_user_id: int = None
) -> List[PostDisplay]:
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found.",
        )

    # Convert posts to PostDisplay objects with like information
    result = []
    for post in user.posts:
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


def count_all_users(db: Session) -> int:
    return db.query(DbUser).count()
