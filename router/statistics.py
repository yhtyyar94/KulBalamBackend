from fastapi import APIRouter, Depends 
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_product, db_user

router = APIRouter(
    prefix='/statistics',
    tags=['statistics']
)

#Count all users
@router.get('/users_count')
def count_all_users(db: Session = Depends(get_db)):
    return {'count': db_user.count_all_users(db)}

#Count all products
@router.get('/products_count')
def count_all_products(db: Session = Depends(get_db)):
    return {'count': db_product.count_all_products(db)}