from typing import List
from db.models import DbUser, DbGroup, group_membership
from schemas import GroupBase, GroupDisplay, GroupMembers
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_group
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)


@router.post("/", response_model=GroupDisplay)
def create_group(group: GroupBase, user_id: int, username: str, db: Session = Depends(get_db)):
    # Create the group in the database
    new_group = db_group.create_group(db=db, request=group, user_id=user_id, username=username)
    # Return the created group
    return new_group


@router.get("/all", response_model=List[GroupDisplay])
def read_groups(db: Session = Depends(get_db)):
    groups = db_group.get_all_groups(db=db)
    group_displays = []
    for group in groups:
        # Extract user IDs from group.members
        member_ids = [member.id for member in group.members]
        group_display = GroupDisplay(
            id=group.id,
            name=group.name,
            description=group.description,
            created_at=group.created_at,
            creator_id=group.creator_id,
            members=member_ids,  # Populate members with user IDs
            visibility=group.visibility
        )
        group_displays.append(group_display)
    return group_displays

@router.get("/{id}", response_model=GroupDisplay)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = db_group.get_group(db=db, group_id=group_id)
    
    # Extract user IDs from group.members
    member_ids = [member.id for member in group.members]
    
    return GroupDisplay(
        id=group.id,
        name=group.name,
        description=group.description,
        created_at=group.created_at,
        creator_id=group.creator_id,
        members=member_ids,  # Pass only integer IDs
        visibility=group.visibility
    )


@router.get("/{id}/members", response_model=List[GroupMembers])
def get_group_members(id: int, db: Session = Depends(get_db)):
    group = db.query(DbGroup).filter(DbGroup.id == id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    members_with_usernames = db.query(DbUser.username).join(group_membership).filter(group_membership.c.group_id == id).all()
    member_list = [{"username": member[0]} for member in members_with_usernames]
    
    return member_list

@router.put("/{id}", response_model=GroupDisplay) 
def update_group(id: int, group: GroupBase, db: Session = Depends(get_db)):
    return db_group.update_group(db=db, group_id=id, request=group)

@router.delete("/{id}", response_model=str)
def delete_group(id: int, db: Session = Depends(get_db), current_user: DbUser  = Depends(get_current_user)):
    return db_group.delete_group(db=db, group_id=id)
