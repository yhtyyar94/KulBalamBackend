from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db import db_group_post
from db.models import group_membership
from schemas import GroupPostBase, GroupPostDisplay, GroupPostUpdate, UserBase
from typing import List

router = APIRouter(
    prefix='/group_posts',
    tags=['groups_posts']
)

def is_member(db: Session, user_id: int, group_id: int) -> bool:
    """
    Checks if a user is a member of a group.
    """
    query = db.query(group_membership).filter(
        group_membership.c.user_id == user_id,
        group_membership.c.group_id == group_id
    )
    return db.query(query.exists()).scalar()

@router.post('', response_model=GroupPostDisplay)
def create_group_post(request: GroupPostBase, db: Session = Depends(get_db)):
    # Check if the user is a member of the group
    user_id = request.author_id
    group_id = request.group_id
    if not is_member(db, user_id, group_id):
        raise HTTPException(status_code=403, detail="User is not a member of the group")

    return db_group_post.create_group_post(db, request)

@router.get('/all', response_model=List[GroupPostDisplay])
def get_group_posts(group_id: int, db: Session = Depends(get_db)):
    group_posts = db_group_post.get_group_posts_by_group_id(db, group_id)
    return group_posts

@router.get('/{id}', response_model=GroupPostDisplay)
def get_group_post(id: int, db: Session = Depends(get_db)):
    group_post = db_group_post.get_group_post(db, id)
    if not group_post:
        raise HTTPException(status_code=404, detail=f"Group post with id {id} not found")
    return group_post

@router.put('/{id}', response_model=GroupPostDisplay)
def update_group_post(group_id: int, post_id: int, request: GroupPostUpdate, user_id: int, db: Session = Depends(get_db)):
    # Retrieve the group post from the database
    group_post = db_group_post.get_group_post(db, post_id)
    
    # Check if the user is the author of the post and the group ID matches
    if group_post.author_id != user_id or group_post.group_id != group_id:
        raise HTTPException(status_code=403, detail="User is not the author of the post or group ID does not match")
    
    # Update the group post
    updated_post = db_group_post.update_group_post(db, post_id, request)
    
    return updated_post

@router.delete('/{id}')
def delete_group_post(group_id: int, post_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    group_post = db_group_post.get_group_post(db, post_id)
    if group_post.group_id != group_id:
        raise HTTPException(status_code=403, detail="Post does not belong to the specified group")
    if not is_member(db, user_id, group_id):
        raise HTTPException(status_code=403, detail="User is not a member of the group")
    return db_group_post.delete_group_post(db, post_id)

