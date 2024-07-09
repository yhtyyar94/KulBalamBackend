from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm.session import Session
from db import db_product_images

router = APIRouter(
    prefix = '/images',
    tags=['images']
)

@router.get('/{id}')
def get_image(id: int, db: Session = Depends (get_db)):
    return db_product_images.get_product_image(db, id)

@router.delete('/{id}')
def delete_image(id:int, db:Session = Depends(get_db)):
    return db_product_images.delete_product_image(db, id)