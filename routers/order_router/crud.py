from ..delivery_router.crud import read_delivery_option_by_id, read_location_by_id
from ..product_router.crud import read_product_by_id
from ..promo_router.crud import read_promo_by_id
from ..users_router.crud import read_user_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

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

#////////////////////////////////

async def create_order(payload:schemas.CreateOrder, preview:bool, db:Session):
    # validate -> owner_id, voucher_id[if present]
    if not await read_user_by_id(payload.owner_id, db):
        pass
        # raise HTTPException(status_code=404, detail="user not found")
    if payload.voucher_id and await read_promo_by_id(payload.voucher_id, db):
        pass
        # raise HTTPException(status_code=404, detail="voucher not found")

    # use delivery address to and delivery price to generate delivery
    if not await read_delivery_option_by_id(payload.delivery_option_id, db):
        pass
        # raise HTTPException(status_code=404, detail="delivery option not found")
    if not await read_location_by_id(payload.delivery_address.location_id, db):
        pass
        # raise HTTPException(status_code=404, detail="location not found")

    # use order items to generate oreder bill
    for item in payload.order_items:
        # get product
        pass
    
    try:
        # print(type(payload.delivery_address))
        pass
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

    # delivery = models.Delivery(**payload.dict(exclude={'delivery_address'}))
    # db.add(delivery) 
    # db.flush()
    # delivery_address = models.DeliveryAddress(**payload.delivery_address.dict(), delivery_id=delivery.id)
    # -----------------------------------------------------------------
    # ////////
    # p = Parent() ... order
    # a = Association(extra_data="some data") ... create order_item object
    # a.child = Child() ... add product to order_item object product
    # p.children.append(a) ... add order_item object to order
    # 1. validate payload
    # 1. create order bill
    # 2. make payments
    # 3. create order
    # 4. create delivery and add to order
    # 5. create payment and add to order
    pass

async def read_orders():
    pass

async def read_order_by_id():
    pass

async def update_order():
    pass

async def delete_order():
    pass


# create order
# read orders/user/location
# read order by id
# update order/order state
# delete order
