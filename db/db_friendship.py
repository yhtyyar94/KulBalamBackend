from fastapi import Response
from sqlalchemy.orm import Session
from db.models import DbUser, DbFriendship
from schemas import FriendshipCreate, Friendship
from typing import List

def get_user(db: Session, user_id: int):
    return db.query(DbUser).filter(DbUser.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DbUser).offset(skip).limit(limit).all()

def create_friendship(db: Session, friendship: FriendshipCreate):
    db_friendship = DbFriendship(**friendship.dict())
    db.add(db_friendship)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship

def get_friend_request(db: Session, friendship_id: int):
    print(friendship_id)
    """Retrieve a friend request by ID."""
    return db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()


def delete_friend_request(db: Session, friendship_id: int):
    """Delete a friend request."""
    friendship = db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return friendship
    return Response(status_code=204)


def delete_friendship(db: Session, friendship_id: int):
    friendship = db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return friendship
    return Response(status_code=204)


def get_friendship_by_users(db: Session, user_id: int, friend_id: int):
    """Retrieve a friendship by user IDs."""
    return db.query(DbFriendship).filter(
        ((DbFriendship.user_id == user_id) & (DbFriendship.friend_id == friend_id)) |
        ((DbFriendship.user_id == friend_id) & (DbFriendship.friend_id == user_id))
    ).first()

def get_friendship_by_user(db: Session, user_id: int, friend_id: int):
    """Retrieve a friendship by user IDs."""
    return db.query(DbFriendship).filter(
        ((DbFriendship.user_id == user_id) & (DbFriendship.friend_id == friend_id)) |
        ((DbFriendship.user_id == friend_id) & (DbFriendship.friend_id == user_id))
    ).all()