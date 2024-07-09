from db.models import DbUser
from schemas import CommentBase, UserAuth, UserBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comment"]
)

@router.get('/all/{post_id}')  # Update the route to accept a post_id parameter
def comment(post_id: int, db: Session = Depends(get_db)):
    return db_comment.get_all(db, post_id)

@router.post('')
def create_comment(request: CommentBase, db: Session = Depends(get_db)):
    return db_comment.create_comment(db, request)

#Delete Post
@router.delete('/{id}')
def delete_comment(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_comment.delete_comment(db, id)