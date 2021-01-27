from ..delivery_router.crud import read_delivery_option_by_id, read_country_by_id, read_sub_country_by_id, read_location_by_id
from ..purchase_type_router.crud import read_purchase_type_by_id
from ..product_router.crud import read_product_by_id
from ..promo_router.crud import read_promo_by_id
from ..users_router.crud import read_user_by_id
from ..location_router.models import Location, SubCountry, Country
from exceptions import UnAcceptableError, NotFoundError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys, utils

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
            if len(order_state.orders.all()):
                raise UnAcceptableError('cannot delete order state with children') 
            db.delete(order_state)
        db.commit()
        return True
    except UnAcceptableError:
        raise HTTPException(status_code=406, detail="{}".format(sys.exc_info()[1]))
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def create_order(payload:schemas.CreateOrder, preview:bool, db:Session):
    total=0
    try:        
        default_order_state = db.query(models.OrderState).filter(models.OrderState.default == True).first()
        test = (await read_user_by_id(payload.owner_id, db), not(utils.logical_xor(payload.voucher_id, await read_promo_by_id(payload.voucher_id, db))), await read_delivery_option_by_id(payload.delivery.delivery_option_id, db), await read_location_by_id(payload.delivery.delivery_address.location_id, db), default_order_state)
        if not all(test):
            raise NotFoundError('{}'.format('user not found' if not test[0] else 'voucher not found' if not test[1] else 'delivery option not found' if not test[2] else 'delivery location not found' if not test[3] else 'default order state not found'))
            
        order = models.Orders(**payload.dict(exclude={'delivery','order_items','voucher_id','payment_info'}), order_state_id=default_order_state.id)
        db.flush()
        delivery = models.Delivery(**payload.delivery.dict(exclude={'delivery_address','order_id'}), order_id=order.id)
        db.add(delivery)  
        delivery_address = models.DeliveryAddress(**payload.delivery.delivery_address.dict(), delivery_id=delivery.id)
        db.add(delivery_address) 
        
        # order_items
        for item in payload.order_items:
            product = await read_product_by_id(item.product_id, db)
            if product:
                if item.quantity >= product.available_quantity:
                    item.quantity = product.available_quantity
                product.available_quantity -= item.quantity
                payment_info = next((info for info in product.payment_info if info.purchase_type_id == item.purchase_type_id), None)
                if item.quantity%payment_info.batch_size != 0:
                    raise UnAcceptableError('invalid purchase quantity selected for {}'.format(product.title))
                if not payment_info:   
                    raise HTTPException(status_code=404, detail="purchase type seleced for product with id {} not valid".format(product.id))
                total+=item.quantity/payment_info.batch_size * payment_info.batch_price

        if payload.voucher_id:
            voucher = await read_promo_by_id(payload.voucher_id, db)
            total -= voucher.discount

        # payment
        # wait for stripe payment
        payment = models.Payment(**payload.payment_info.dict(exclude={'card'}), card_number_brand=payload.payment_info.card.number.brand, card_number_masked=payload.payment_info.card.number.masked, amount=total)
        db.add(payment)
        order_bill = models.OrderBill(amount=total, order_id=order.id, payment=payment)
        db.add(order_bill)
        db.add(order) 
        db.commit()   
        db.refresh(order)     
        return order
    except UnAcceptableError:
        raise HTTPException(status_code=422, detail="{}".format(sys.exc_info()[1]))
    except NotFoundError:
        raise HTTPException(status_code=404, detail="{}".format(sys.exc_info()[1]))
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))

async def read_orders(skip:int, limit:int, search:str, value:str, location_id:int, sub_country_id:int, country_id:int, order_state_id:int, user_id:int, db: Session):
    base = db.query(models.Orders)
    if country_id and await read_country_by_id(country_id, db):
        base = base.join(Location).join(SubCountry).join(Country).filter(Country.id==country.id)
    elif sub_country_id and await read_sub_country_by_id(sub_country_id, db):
        base = base.join(Location).join(SubCountry).filter(SubCountry.id == sub_country_id)
    elif location_id and await read_location_by_id(location_id, db):
        base = base.join(Location).filter(Location.id == location_id) 

    if order_state_id and await read_order_state_by_id(order_state_id, db):
        base = base.filter(models.Orders.order_state_id==order_state_id)
    if user_id and await read_user_by_id(user_id, db):
        base = base.filter(models.Orders.owner_id==user_id)

    if search and value:
        try:
            base = base.filter(models.Orders.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_order_by_id(id:int, db:Session):
    return db.query(models.Orders).filter(models.Orders.id==id).first()

async def delete_order(id:int, db:Session):
    try:
        order = await read_order_by_id(id, db)        
        if order:
            db.delete(order)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

#////////////////////////////////
async def update_order():
    pass

# create order
# read orders/user/location
# read order by id
# update order/order state
# delete order
# test = [1,2,3,4,5,6,7,5,4.54]
# test2 = [{'a':45},{'a':3},{'a':1},{'a':12},{'a':78},{'a':43},{'a':5},]
# res = sum(test)
# res2 = sum(item['a'] for item in test2)