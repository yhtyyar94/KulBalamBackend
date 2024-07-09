import random
from fastapi import APIRouter, Depends 
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_product, db_user
from schemas import ProductBase, UserBase, TestProductBase

router = APIRouter(
    tags=[]
)

@router.post('/test_data/all')
def create_data(db: Session = Depends(get_db)):
    create_users(db)
    create_products(db)
    return {'created': True}

def create_users(db: Session):
    for name in ('maria', 'sefika', 'amir', 'saskia', 'joan', 'joep'):
        user = UserBase(username=name, email=f'{name}@gmail.com', password='string12.')
        db_user.create_user(db, user)

def create_products(db: Session):
    for name in ('camera', 'watch', 'laptop', 'smart phone'):
        product = TestProductBase(
            product_name=name,
            description='good quality',
            price=random.randint(100,200),
            quantity=random.randint(1,10), 
            published=True,
            seller_id=random.randint(1,6)
        )
        db_product.test_products(db, product, user_id=product.seller_id)
    return {'created': True}

@router.post('/test_data/products')
def create_products(db: Session = Depends(get_db)):
    for name in ('camera', 'watch', 'laptop', 'smart phone'):
        product = TestProductBase(
            product_name=name,
            description='good quality',
            price=random.randint(100,200),
            quantity=random.randint(1,10), 
            published=True,
            seller_id=random.randint(1,6)
        )
        db_product.test_products(db, product, user_id=product.seller_id)
    return {'created': True}