from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile
from auth.oauth2 import get_current_user
from schemas import ProductBase, ProductDisplay, ProductImage, Review, ReviewDisplay, UserBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_product, db_product_images, db_review, db_product
import string
import random
import shutil

router = APIRouter(
    prefix='/products',
    tags=['products']
)

#Insert product
@router.post('/', response_model=ProductDisplay)
def insert_product(request: ProductBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_product.insert_product(db, request, current_user.id)

#Get a product by id
@router.get('/{id}', response_model=ProductDisplay)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return db_product.get_product_by_id(db, id)

#Get products
@router.get('/', response_model=List[ProductDisplay])
def get_product( db: Session = Depends (get_db), product_name: str='', user_products: bool=False, price_order: Optional[str]=None,
                current_user: UserBase = Depends(get_current_user)): #str='' for query parameter
    user_id = current_user.id if user_products else None
    return db_product.get_all_products(db, product_name, user_id, price_order)

#Update a product
@router.put('/{id}',  response_model=ProductDisplay)
def update_product(id: int, product_name: str, description: str, price: float, quantity: int, db: Session = Depends (get_db)):
    return db_product.update_product(db, id, product_name,description, price, quantity )

#Delete a product
@router.delete('/{id}')
def delete_product(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_product.delete_product(db, id, current_user.id)

#Inert image
@router.post('/{id}/images', response_model=ProductImage)
def upload_product_image(id: int, image: UploadFile = File(...), db: Session = Depends (get_db)):
    return db_product_images.upload_product_image(db, id, image)

#Create product review
@router.post('/{id}/reviews', response_model=ReviewDisplay)
def create_review(id: int, request: Review, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_review.create_review(db, id, current_user.id, request)

#Get all reviews of a product
@router.get("/{id}/reviews", response_model=List[ReviewDisplay])
def get_reviews(id: int, db: Session = Depends(get_db)):
    reviews = db_review.get_all_product_reviews(db, id)
    return reviews