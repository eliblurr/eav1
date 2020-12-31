from ..product_router.crud import read_product_by_id
from helper import FolderIO, ImageFolderIO
from sqlalchemy.orm import Session
from fastapi import HTTPException
from static.main import event_DIR
from . import models, schemas
from sqlalchemy import exc
from typing import List
import utils
import sys

folder_io = FolderIO(event_DIR)
image_folder_io = ImageFolderIO(event_DIR, 15, folder_io, 'events')

async def create_event(payload: schemas.CreateEvent, images, db: Session):
    try:
        urls, folder_name = await image_folder_io.create(images, 700, 500)
        new_event = models.Events(**payload.dict())
        db.add(new_event) 
        db.flush()
        for url in urls:
            url = models.EventImages(image_url=url, folder_name=folder_name)
            new_event.images.append(url)
        db.commit()
        db.refresh(new_event)
        return new_event
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
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

async def read_event_products(id:int, skip: int, limit: int, search:str, value:str, db: Session):
    base = await read_event_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.event_items
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def update_event(id: int, payload: schemas.UpdateEvent, db: Session):
    if not await read_event_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Events).filter(models.Events.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_event_by_id(id, db)
    except IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_event(id: int, db: Session):
    try:
        event = await read_event_by_id(id, db)
        if event and len(event.images):
            await utils.delete_folder(event_DIR+"/"+event.images[0].folder_name)
            db.delete(event)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_event_image(id: int, images, db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404)
    try:
        urls, folder_name = await image_folder_io.append_image(event, images, 700, 500)
        if urls and folder_name:
            for url in urls:
                url = models.EventImages(image_url=url, folder_name=folder_name)
                event.images.append(url)
        db.commit()
        db.refresh(event)
        return event
    except:      
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_event_image(id: int, db:Session):
    event_image = db.query(models.EventImages).filter(models.EventImages.id == id).first()
    try: 
        if event_image:
            _ , folder_name, image_name = event_image.image_url.split("/")
            if await utils.file_exists(event_DIR+"/"+folder_name+"/"+image_name) and await utils.delete_file(event_DIR+"/"+folder_name+"/"+image_name):
                db.delete(event_image)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_item_to_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404)
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product and (product not in event.event_items):
                event.event_items.append(product)
            else:
                pass
        db.commit()
        db.refresh(event)
        return event
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409) #product already exists for 
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_product_from_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404)
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product:
                event.event_items.remove(product)
        db.commit()
        db.refresh(event)
        return event
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)