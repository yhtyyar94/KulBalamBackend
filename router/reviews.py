from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from schemas import ProductBase, ProductDisplay, Review, ReviewDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_review

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

#Get a review by id
@router.get('/{id}')
def get_review_by_id(id: int, db: Session = Depends(get_db)):
    return db_review.get_review_by_id(db, id)

#Update a review
@router.put('/{id}')
def update_review(id: int, score: int, comment: str, db: Session = Depends(get_db)):
    return db_review.update_review(db, id, score, comment)

#Delete a review
@router.delete('/{id}')
def delete_review(id:int, db:Session = Depends(get_db)):
    return db_review.delete_review(db, id)