from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_
from typing import List

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id

from ..product_router.models import Products

from static.main import static_DIR

# create event
# delete event
# remove item from event
# add item to event
# update event details
# read event
# read event profducts

async def create_event(payload: schemas.CreateEvents, images, db: Session):

    urls = []

    try:
        for file in images:
            image = await file.read()
            image_id =  utils.gen_alphanumeric_code_lower(length=25)
            _type = file.content_type.split('/')
            image_url = '/e7v0ccwr0ua4c/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )

            if not _type[0] == 'image':
                continue

            if await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), image):
                urls.append(image_url)
        
    except:
        raise HTTPException(status_code=500, detail="failed to upload images")

    try:  
        new_event = models.Events(**payload.dict())
        db.add(new_event) 
        db.flush()

        if len(urls):
            for url in urls:
                url = models.EventImages(image_url='{static_DIR}{url}'.format(static_DIR=static_DIR,url=url))
                new_event.images.append(url)

        db.commit()
        db.refresh(new_event)
        return new_event

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def delete_event(id: int, db: Session):
    try:
        event = await read_event_by_id(id, db)
        if event:
            for image in event.images:
                utils.delete_file(image.image_url)
            db.delete(event)
            db.commit()
        return True

    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_item_to_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id,db)
    if not event:
        raise HTTPException(status_code=404, detail="could not find event")
    
    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                event.event_items.append(product)
        
        db.commit()
        db.refresh(event)
        return event

    except IntegrityError as e:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed, product already part of event")

    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def remove_item_from_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id,db)
    if not event:
        raise HTTPException(status_code=404, detail="could not find event")
    
    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                event.event_items.remove(product)

        db.commit()
        db.refresh(event)
        return event
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def add_image_to_event(id: int, image, db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="could not find event")

    try:
        _image = await image.read()
        image_id = utils.gen_alphanumeric_code_lower(length=20)
        _type = image.content_type.split('/')
        image_url = '/e7v0ccwr0ua4c/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )
            
        if not _type[0] == 'image':
            raise HTTPException(status_code=422)

        if not await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), _image):
            raise HTTPException(status_code=500, detail="failed to upload image")    
    except:
        raise HTTPException(status_code=500, detail="failed to upload images")

    try:
        url = models.EventImages(image_url='{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url))
        event.images.append(url)
        db.commit()
        db.refresh(event)
        return event
    except:
        db.rollback()
        raise HTTPException(status_code=500)
        

async def update_event_details(id: int, payload: schemas.UpdateEvents, db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404)

    try:
        db.query(models.Events).filter(models.Events.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_event_by_id(id, db)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
 
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)


async def read_event(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Events)
    if search and value:
        try:
            base = base.filter(models.Events.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_event_by_id(id: int, db: Session):
    return db.query(models.Events).filter(models.Events.id == id).first()

async def remove_image_from_event(id: int, image_id, db:Session):
    event = await read_event_by_id(id, db)
    if event is None:
        raise HTTPException(status_code=404)

    image = db.query(models.EventImages).filter(and_(
        models.EventImages.id == image_id,
        models.EventImages.event_id == id
    )).first()

    if image is None:
        raise HTTPException(status_code=404)

    try:
        utils.delete_file('{image_url}'.format(image_url=image.image_url))
        db.delete(image)
        db.commit()

    except:
        db.rollback()
        raise HTTPException(status_code=500)
    
    db.refresh(event)
    return event

async def read_event_products(id: int, skip: int, limit: int, db: Session):
    if not await read_event_by_id(id, db):
        raise HTTPException(status_code=404)
    return db.query(models.Events).filter(models.Events.id == id).first().event_items.offset(skip).limit(limit).all()