from sqlalchemy.orm import Session
from db.database import Base

# Define the association table for many-to-many relationship
group_membership = Base.metadata.tables['group_membership']

# Add a user to a group
def join_group(db: Session, group_id: int, user_id: int, membership_id: int, username: str):
    db.execute(group_membership.insert().values(group_id=group_id, user_id=user_id, membership_id=membership_id, username=username))
    db.commit()