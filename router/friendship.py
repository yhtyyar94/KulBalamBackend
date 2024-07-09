from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_friendship import create_friendship, delete_friend_request, get_friend_request, get_friendship_by_users
from db.models import DbFriendship, DbUser
from schemas import FriendshipCreate, Friendship
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db

router = APIRouter(
    tags=["friendships"]
)


@router.post("/friendships", response_model=Friendship)
def send_friend_request(from_user_id: int, to_user_id: int,sender_username: str, db: Session = Depends(get_db)):
    """Send a friend request from one user to another."""
    friendship = get_friendship_by_users(db, from_user_id, to_user_id)
    if friendship:
        raise HTTPException(status_code=400, detail="Friendship request already exists")

    friendship_data = FriendshipCreate(user_id=from_user_id, friend_id=to_user_id,sender_username=sender_username)
    friendship_to_data =FriendshipCreate(user_id=to_user_id, friend_id=from_user_id,sender_username=sender_username)
    res= create_friendship(db, friendship_data)
    create_friendship(db, friendship_to_data)
    friendship = get_friend_request(db, res.id)
    friendship.accepted = True
    db.commit()
    return res


@router.get("/friendshiprequests", response_model=List[Friendship])
def get_friend_requests(user_id: int, db: Session = Depends(get_db)):
    """Get all friend requests for a given user."""
    friend_requests = db.query(DbFriendship).filter(DbFriendship.user_id == user_id, DbFriendship.accepted == False).all()
    return friend_requests

@router.put("/friendships/{id}", response_model=Friendship)
def update_friendship_status(id: int, status: str, db: Session = Depends(get_db)):
    """Update the status of a friendship request."""
    friendship = get_friend_request(db, id)
    if friendship:
        if status.lower() == "accept":
            friendship.accepted = True
            db.commit()
            return friendship
        elif status.lower() == "reject":
            delete_friend_request(db,id)
            return friendship
        else:
            raise HTTPException(status_code=400, detail="Invalid status. Use 'accept' or 'reject'.")
    raise HTTPException(status_code=404, detail="Friendship request not found")


@router.delete("/friends/{friendship_id}")
def unfriend(friendship_id: int, db: Session = Depends(get_db)):
    """Remove a friendship."""
    friendship = db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()
    if friendship:
        # Delete the friendship from the first user's perspective
        db.delete(friendship)
        
        # Find the corresponding friendship from the other user's perspective
        inverse_friendship = db.query(DbFriendship).filter(
            (DbFriendship.user_id == friendship.friend_id) &
            (DbFriendship.friend_id == friendship.user_id)
        ).first()
        
        if inverse_friendship:
            # Delete the friendship from the other user's perspective
            db.delete(inverse_friendship)
        
        db.commit()
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Friendship not found")

    
