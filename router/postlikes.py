from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_postlikes
from auth.oauth2 import get_current_user
from schemas import UserBase

router = APIRouter(prefix="/postlikes", tags=["postlikes"])


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    """Allow a user to like a post. Users cannot like their own posts."""
    return db_postlikes.create_like(db, post_id, current_user.id)


@router.delete("/{post_id}")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    """Allow a user to unlike a post they previously liked."""
    return db_postlikes.delete_like(db, post_id, current_user.id)
