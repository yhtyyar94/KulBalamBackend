from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session 
from db.models import DbOrder, DbOrderLine, DbUser, DbProduct
from enums import OrderStatus
from schemas import Order, MinOrderLine
from sqlalchemy import func

def create_empty_order (db: Session, user_id):
    existing_order = db.query(DbOrder).filter(
        DbOrder.user_id == user_id,
        DbOrder.order_status == OrderStatus.PENDING
    ).first()

    if existing_order:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pending order already exists for user with ID '{user_id}'."
        )

    buyer = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buyer with ID '{user_id}' not found."
        )

    new_order = DbOrder(
        order_status = OrderStatus.PENDING, 
        user_id = buyer.id,
        total = 0
    )
    db.add(new_order) 
    db.commit()
    db.refresh(new_order)
    return new_order


def create_order (db: Session, order_status, user_id):
    buyer = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buyer with ID '{user_id}' not found."
        )

    new_order = DbOrder(
        order_status = order_status, 
        user_id = user_id,
        total = 0
    )
    db.add(new_order) 
    db.commit()
    db.refresh(new_order)
    return new_order

#Creates a shopping cart
def get_or_create_order_by_user(db: Session, user_id, order_status: OrderStatus):
    order = db.query(DbOrder).\
        filter(DbOrder.user_id == user_id, DbOrder.order_status == order_status).\
        first()
    if not order:
        return create_order(db,order_status,user_id )
    return order

def get_order(db: Session, order_id: int):
    order = db.query(DbOrder).filter(DbOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id '{order_id}' not found."
        )
    return order

def get_order_line(db: Session, order_line_id: int):
    order_line = db.query(DbOrderLine).filter(DbOrderLine.id == order_line_id).first()
    if not order_line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order line with id '{order_line_id}' not found."
        )
    return order_line

def create_order_line(db: Session, order_id: int, product_id: int, quantity: int):
    product = db.query(DbProduct).filter(DbProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found.")

    order = db.query(DbOrder).filter(DbOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id '{order_id}' not found.")

    total_price = product.price * quantity
    
    existing_product_order_line = db.query(DbOrderLine).filter(DbOrderLine.order_id == order_id, DbOrderLine.product_id == product_id).first()
    
    if existing_product_order_line:
        existing_product_order_line.quantity += quantity
        existing_product_order_line.total += total_price
        order.total += total_price
        db.commit()
        db.refresh(existing_product_order_line)
        return existing_product_order_line
    
    else:
        new_order_line = DbOrderLine(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            total=total_price
        )
    
        db.add(new_order_line)
        order.total += total_price
        db.commit()
        db.refresh(new_order_line)
        return new_order_line

def update_order_line(db: Session, id: int, request: MinOrderLine):
    order_line = db.query(DbOrderLine).filter(DbOrderLine.id == id).first()

    if not order_line:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order line with id '{id}' not found."
        )
    
    previous_total = order_line.total

    #Updates the order line
    order_line.product_id = request.product_id
    order_line.quantity = request.quantity

    # Calculates the new price in order line
    product = db.query(DbProduct).filter(DbProduct.id == order_line.product_id).first()
    total_price = product.price * order_line.quantity
    order_line.total = total_price

    # Updates the order total price
    order = db.query(DbOrder).filter(DbOrder.id == order_line.order_id).first()
    order.total -= previous_total
    order.total += order_line.total

    db.commit()
    db.refresh(order_line)
    db.refresh(order)

    return order_line

def delete_order_line(db: Session, id: int):
    order_line = db.query(DbOrderLine).filter(DbOrderLine.id == id).first()
    if order_line is None:
        raise HTTPException(status_code=404, detail=f"Order line with id '{id}' not found")
    
    order = db.query(DbOrder).filter(DbOrder.id == order_line.order_id).first()
    order.total -= order_line.total

    db.delete(order_line)
    db.add (order)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

def delete_order(db: Session, id: int):
    order = db.query(DbOrder).filter(DbOrder.id == id).first()
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order with id '{id}' not found")
     
    # Deletes order lines attached
    order_lines = db.query(DbOrderLine).filter(DbOrderLine.order_id == id).all()
    for order_line in order_lines:
        db.delete(order_line)

    # Deletes order
    db.delete(order)
    db.commit()

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)