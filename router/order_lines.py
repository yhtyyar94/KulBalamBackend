from fastapi import APIRouter, Depends 
from enums import OrderStatus
from schemas import MinOrderLine, OrderLine, UserBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_orders
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/order_lines',
    tags=['order_lines']
)

#Create order by user
@router.post('/')
def create_order_line(request: MinOrderLine, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    order = db_orders.get_or_create_order_by_user(db, current_user.id, OrderStatus.PENDING)
    return db_orders.create_order_line(db, order.id, request.product_id, request.quantity)

#Get an order line
@router.get('/{id}', response_model=OrderLine)
def get_order_line(id: int, db: Session = Depends (get_db)):
    return db_orders.get_order_line(db, id)

#Update an order line
@router.put('/{id}')
def update_order_line(id: int, request: MinOrderLine, db: Session = Depends(get_db)):
    return db_orders.update_order_line(db, id, request)

#Delete an order line
@router.delete('/{id}')
def delete_order_line(id:int, db:Session = Depends(get_db)):
    return db_orders.delete_order_line(db, id)