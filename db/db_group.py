from sqlalchemy.orm.session import Session
from db.db_join import join_group
from db.models import DbGroup, group_membership
from datetime import datetime
from fastapi import HTTPException, Response, status
from typing import List
from schemas import GroupBase, GroupDisplay, GroupMembers

def create_group(db: Session, request: GroupBase, user_id: int, username: str):
    # Ensure that created_at is set to the current datetime if not provided
    created_at = request.created_at or datetime.now()
    
    # Create a new Group instance with the provided data
    new_group = DbGroup(**request.dict())
    
    # Add the group to the database session and commit the transaction
    db.add(new_group)
    db.commit()
    
    # Refresh the group instance to fetch the generated ID from the database
    db.refresh(new_group)
    
    # Automatically join the user to the group
    join_group(db, group_id=new_group.id, user_id=user_id, membership_id=None, username=username)

    # Return the created group as per GroupDisplay model
    return {
        "id": new_group.id,
        "name": new_group.name,
        "description": new_group.description,
        "created_at": new_group.created_at,
        "creator_id": new_group.creator_id,
        "members": [],  # Assuming the members list is empty initially
        "visibility": new_group.visibility
    }


def get_all_groups(db: Session) -> List[GroupDisplay]:
    groups = db.query(DbGroup).all()
    return groups

def get_group(db: Session, group_id: int) -> GroupDisplay:
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with id {group_id} not found'
        )
    return group

def get_members(db: Session, member_id: int) -> GroupMembers:
    members= db.query(group_membership).filter(group_membership.id == member_id).first()
    return members

def update_group(db: Session, group_id: int, request: GroupBase):
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Group with id {group_id} not found'
        )
    # Update group attributes
    group.name = request.name
    group.description = request.description
    group.is_public = request.is_public
    group.visibility = request.visibility
    db.commit()
    return group  # Return the updated group


def delete_group(db: Session, group_id: int):
    # Fetch the group from the database
    group = db.query(DbGroup).filter(DbGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Group post with id {id} not found') 
    db.delete(group)
    db.commit()
    return Response(status_code=204)
