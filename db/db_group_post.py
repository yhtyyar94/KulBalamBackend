from sqlalchemy.orm import Session
from db.models import DbGroupPost
from schemas import GroupPostBase, GroupPostUpdate
from fastapi import HTTPException, Response, status
import datetime
from typing import List

def create_group_post(db: Session, request: GroupPostBase) -> DbGroupPost:
    new_group_post = DbGroupPost(
        content=request.content,
        group_id=request.group_id,
        author_id=request.author_id,
        created_at=datetime.datetime.now()
    ) 
    db.add(new_group_post)
    db.commit()
    db.refresh(new_group_post)
    return new_group_post

def get_group_posts_by_group_id(db: Session, group_id: int) -> List[DbGroupPost]:
    return db.query(DbGroupPost).filter(DbGroupPost.group_id == group_id).all()

def get_group_post(db: Session, id: int) -> DbGroupPost:
    group_post = db.query(DbGroupPost).filter(DbGroupPost.id == id).first()
    if not group_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Group post with id {id} not found')  
    return group_post

def update_group_post(db: Session, id: int, request: GroupPostUpdate):
    # Retrieve the group post from the database
    group_post = db.query(DbGroupPost).filter(DbGroupPost.id == id).first()
    
    # Check if the group post exists
    if not group_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group post with id {id} not found")

    # Update the group post attributes
    group_post.content = request.content

    # Commit the changes to the database
    db.commit()
    
    # Return the updated group post
    return group_post

def delete_group_post(db: Session, id: int) -> str:
    group_post = db.query(DbGroupPost).filter(DbGroupPost.id == id).first()
    if not group_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Group post with id {id} not found') 
    db.delete(group_post)
    db.commit()
    return Response(status_code=204)
