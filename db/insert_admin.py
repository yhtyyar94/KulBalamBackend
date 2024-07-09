import random
import string
from sqlalchemy.exc import IntegrityError
from db.db_user import create_user
from schemas import UserBase
from .models import DbUser  # Assuming your models are imported from another module
from .hash import Hash  # Assuming your hashing utility is imported from another module
from .database import SessionLocal  # Assuming your database session is imported from another module

'''
def insert_admin():
    db = SessionLocal()
    try:
        admin_exists = db.query(DbUser).filter(DbUser.username == "admin").first() is not None
        if not admin_exists:
            hashed_password = Hash.bcrypt("admin")  # Hash the admin password
            admin_user = DbUser(username="admin", email="Admin@example.com", password=hashed_password)
            db.add(admin_user)
            db.commit()

            print("Admin user created successfully.")
        else:
            print("Admin user already exists. Skipping creation.")
        
        # Define and insert other dummy users if needed
        dummy_users = [
            UserBase(username="Alex", email="Alex@example.com", password="Alex1234!"),
            UserBase(username="Ben", email="Ben!234@example.com", password="Ben1234!"),
        ]

        for user_data in dummy_users:
            user_exists = db.query(DbUser).filter(DbUser.username == user_data.username).first() is not None
            if not user_exists:
                try:
                    create_user(db=db, request=user_data)
                except IntegrityError:
                    print(f"Duplicate user entry detected for {user_data.username}, skipping...")
                    db.rollback()  # Handle duplicate entries by rolling back the transaction
            else:
                print(f"User {user_data.username} already exists. Skipping creation.")

    finally:
        db.close()

'''
