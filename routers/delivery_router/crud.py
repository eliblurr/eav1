from ..location_router.crud import read_location_by_id
from ..timeline_router.crud import read_timeline_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
import sys

async def create_delivery_option(payload: schemas.CreateDeliveryOption, db:Session):
    try:
        delivery_option = models.DeliveryOption(**payload.dict())
        db.add(delivery_option) 
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

async def read_delivery_option(skip:int, limit:int, search:str, value:str, location_id:int, db:Session):
    base = db.query(models.DeliveryOption)
    if location_id:
        location = await read_location_by_id(location_id, db)
        if location is not None:
            base = location.loction_delivery_options
    if search and value:
        try:
            base = base.filter(models.DeliveryOption.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_delivery_by_id(id:int, db:Session):
    return db.query(models.DeliveryOption).filter(models.DeliveryOption.id==id).first()

async def update_delivery_option(id:int, payload:schemas.UpdateDeliveryOption, db:Session):
    if not await read_delivery_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.DeliveryOption).filter(models.DeliveryOption.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_delivery_by_id(id, db)
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
        delivery_option = await read_delivery_by_id(id, db)
        if delivery_option:
            db.delete(delivery_option)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def create_delivery(payload:CreateDelivery, db:Session):
    try:
        delivery = models.Delivery(**payload.dict())
        db.add(delivery) 
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

async def read_delivery(skip:int, limit:int, search:str, value:str, db:Session):
    base = db.query(models.Delivery)
    if search and value:
        try:
            base = base.filter(models.Delivery.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_delivery_by_id(id:int, db:Session):
    return db.query(models.Delivery).filter(models.Delivery.id==id).first()

async def update_delivery(id:int, payload:UpdateDelivery, db:Session):
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
    if not delivery:
        raise HTTPException(status_code=404)
    try:
        delivery_timeline = models.DeliveryTimeline(**payload.dict())
        db.add(delivery_timeline) 
        db.flush()
        delivery.delivery_timeline.append(delivery_timeline)
        db.commit()   
        db.refresh(delivery_timeline)     
        return delivery_timeline
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def toggle_timeline_delivery(id:int, timeline_id:int, db:Session):
    delivery = await read_delivery_by_id(id, db)
    timeline = await read_timeline_by_id(timeline_id, db)
    res = (delivery is not None, timeline is not None)
    if all(res):
        pass
    except:
        raise HTTPException(status_code=404, detail="{} not found".format('delivery' if not(res[0]) else 'timeline'))
    try:
        if timeline not in delivery.delivery_timeline:
            delivery.delivery_timeline.append(timeline)
            state = 'added'
        else:
            delivery.delivery_timeline.remove(timeline)
            state = 'removed'
        db.commit()
        db.refresh(delivery)
        return True, state
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:      
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_delivery_timeline(id:int, skip:int, limit:int, db:Session):
    delivery = await read_delivery_by_id(id, db)
    if not delivery:
        raise HTTPException(status_code=404)
    return delivery.delivery_timeline.offset(skip).limit(limit).all()