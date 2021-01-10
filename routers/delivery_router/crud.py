from services.pricing import calculate_delivery_option_price
from ..location_router.crud import read_location_by_id
from ..timeline_router.crud import read_timeline_by_id
from sqlalchemy.orm import Session, exc as orm_exc
from fastapi import HTTPException
from sqlalchemy import exc, and_
from . import models, schemas
from typing import List
import sys

# delivery options
async def create_delivery_option(payload: schemas.CreateDeliveryOption, db:Session):
    try:
        delivery_option = models.DeliveryOption(**payload.dict(exclude={'location_ids'}))
        db.add(delivery_option) 
        db.flush()
        for id in payload.location_ids:
            location = await read_location_by_id(id, db)
            if location:
                delivery_option.locations.append(location)
        db.commit()   
        db.refresh(delivery_option)     
        return delivery_option
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_delivery_option(skip:int, limit:int, search:str, value:str, location_id:int, total_weight_in_kg:float, db:Session):
    base = db.query(models.DeliveryOption)
    if location_id:
        location = await read_location_by_id(location_id, db)
        if location is not None:
            base = location.loction_delivery_options
    if search and value:
        try:
            base = base.filter(models.DeliveryOption.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            res = base.offset(skip).limit(limit).all()
    res = base.offset(skip).limit(limit).all()
    if total_weight_in_kg:
        for item in res:
            item.price_to_pay = await calculate_delivery_option_price(total_weight_in_kg, item.rate)
    return res

async def read_delivery_option_by_id(id:int, db:Session):
    return db.query(models.DeliveryOption).filter(models.DeliveryOption.id==id).first()

async def update_delivery_option(id:int, payload:schemas.UpdateDeliveryOption, db:Session):
    if not await read_delivery_option_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.DeliveryOption).filter(models.DeliveryOption.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_delivery_option_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_delivery_option(id:int, db:Session):
    try:
        delivery_option = await read_delivery_option_by_id(id, db)
        if delivery_option:
            db.delete(delivery_option)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_location_to_delivery_option(id:int, location_ids:List[int], db:Session):
    delivery_option = await read_delivery_option_by_id(id, db)
    if not delivery_option:
        raise HTTPException(status_code=404)
    try:
        for id in location_ids:
            location = await read_location_by_id(id, db)
            if location:
                delivery_option.locations.append(location)
        db.commit()
        db.refresh(delivery_option)
        return delivery_option
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_location_from_delivery_option(id:int, location_ids:List[int], db:Session):
    delivery_option = await read_delivery_option_by_id(id, db)
    if not delivery_option:
        raise HTTPException(status_code=404)
    try:
        for id in location_ids:
            location = await read_location_by_id(id, db)
            if location:
                delivery_option.locations.remove(location)
        db.commit()
        db.refresh(delivery_option)
        return delivery_option
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

# ///////////////////////////////////
# delivery
async def create_delivery(payload:schemas.CreateDelivery, db:Session):
    if not await read_delivery_option_by_id(payload.delivery_option_id, db):
        raise HTTPException(status_code=404, detail="delivery option not found")
    if not await read_location_by_id(payload.delivery_address.location_id, db):
        raise HTTPException(status_code=404, detail="location not found")
    try:
        delivery = models.Delivery(**payload.dict(exclude={'delivery_address'}))
        db.add(delivery) 
        db.flush()
        delivery_address = models.DeliveryAddress(**payload.delivery_address.dict(), delivery_id=delivery.id)
        db.add(delivery_address) 
        db.commit()   
        db.refresh(delivery)     
        return delivery
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_delivery(skip:int, limit:int, search:str, value:str, location_id:int, db:Session):
    base = db.query(models.Delivery)
    if location_id:
        base = base.join(models.DeliveryAddress).join(models.Location).filter(models.Location.id == location_id)
    if search and value:
        try:
            base = base.filter(models.Delivery.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_delivery_by_id(id:int, db:Session):
    return db.query(models.Delivery).filter(models.Delivery.id==id).first()

async def update_delivery(id:int, payload:schemas.UpdateDelivery, db:Session):
    if not await read_delivery_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Delivery).filter(models.Delivery.id==id).update(payload.dict(exclude_unset=True).items())
        db.commit()
        if updated:
            return await read_delivery_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_delivery(id:int, db:Session):
    try:
        delivery = await read_delivery_by_id(id, db)
        if delivery:
            db.delete(delivery)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def create_delivery_timeline(id:int, payload:schemas.CreateDeliveryTimeline, db:Session):
    delivery = await read_delivery_by_id(id, db)
    timeline = await read_timeline_by_id(payload.timeline_id, db)
    if not timeline:
        raise HTTPException(status_code=404, detail="timeline not found")
    if timeline.title=='custom' and payload.title=='':
        raise HTTPException(status_code=422, detail="title required for custom timeline")
    if not delivery:
        raise HTTPException(status_code=404, detail="delivery not found")
    try:
        delivery_timeline = models.DeliveryTimeline(**payload.dict(exclude={'timeline_id'}), timeline=timeline)
        delivery.timeline.append(delivery_timeline)
        db.commit()
    except orm_exc.FlushError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_delivery_timeline(id:int, timeline_id:int, index:int, db:Session):
    delivery_timeline = db.query(models.DeliveryTimeline).filter(
        and_(
            models.DeliveryTimeline.delivery_id==id,
            models.DeliveryTimeline.timeline_id==timeline_id,
            models.DeliveryTimeline.index==index,
        )
    ).first()
    try:
        if delivery_timeline:
            db.delete(delivery_timeline)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_delivery_timeline(id:int, skip:int, limit:int, db:Session):
    delivery = await read_delivery_by_id(id, db)
    if not delivery:
        raise HTTPException(status_code=404)
    return delivery.timeline
    # .all()
    # .offset(skip).limit(limit).all()