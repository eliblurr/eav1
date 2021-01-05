from ..product_router.crud import read_product_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

async def create_order():
    pass

async def read_orders():
    pass

async def read_order_by_id():
    pass

async def update_order():
    pass

async def delete_order():
    pass

async def create_order_state(payload:schemas.CreateOrderState, db:Session):
    try:
        order_state = models.OrderState(**payload.dict())
        db.add(order_state) 
        db.commit()   
        db.refresh(order_state)     
        return order_state
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code = 500)

async def read_order_states(skip:int, limit:int, search:str, value:str, db: Session):
    base = db.query(models.OrderState)
    if search and value:
        try:
            base = base.filter(models.OrderState.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_order_state_by_id(id:int, db:Session):
    return db.query(models.OrderState).filter(models.OrderState.id==id).first()

async def update_order_state(id:int, payload:schemas.UpdateOrderState, db:Session):
    if not await read_order_state_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.OrderState).filter(models.OrderState.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_order_state_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_order_state(id:int, db:Session):
    try:
        order_state = await read_order_state_by_id(id, db)
        if order_state:
            db.delete(order_state)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

# create order
# read orders/user/location
# read order by id
# update order/order state
# delete order
