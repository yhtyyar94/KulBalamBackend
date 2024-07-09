from datetime import datetime
from sqlalchemy.orm import Session
from db.models import DbComment, DbPost
from schemas import CommentBase
from fastapi import HTTPException, Response, status


def create_comment(db: Session, request: CommentBase):
    # Check if the specified post_id exists
    post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {request.post_id} not found')

    # Create the comment associated with the specified post
    new_comment = DbComment(
        text=request.txt,
        username=request.username,
        user_id = request.user_id,
        post_id=request.post_id,
        timestamp=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()  # Use post_id to filter comments


def delete_comment(db:Session, id: int):
    comment =  db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f'Comment with id {id} not found') 
    db.delete(comment)
    db.commit()
    return Response(status_code=204)


