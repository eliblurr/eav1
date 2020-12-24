from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..product_router.crud import read_products_by_id
from ..product_router.models import Products
from helper import ImageIO, FolderIO
from sqlalchemy import update, and_
from sqlalchemy.orm import Session
from static.main import event_DIR
from fastapi import HTTPException
from . import models, schemas
from main import get_db
from typing import List
import utils
import sys

folder_io = FolderIO(event_DIR)

async def create_event(payload: schemas.CreateEvent, images, db: Session):
    urls = []
    try:
        folder_name = utils.gen_alphanumeric_code_lower(length=15)
        while await utils.folder_exists(event_DIR+"/"+folder_name):
            continue
        
        if not await folder_io.create(folder_name):
            raise HTTPException(status_code=500, detail="failed to create image store dir")

        image_io = ImageIO(await folder_io._directory())

        for image in images:
            ftype, fext = image.content_type.split('/')
            fn = "img_"+str(images.index(image)+1)
            image_b = await image.read()

            if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 480, 704):
                urls.append("events/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext) )

        new_event = models.Events(**payload.dict())
        db.add(new_event) 
        db.flush()

        if len(urls):
            for url in urls:
                url = models.EventImages(image_url=url, folder_name=folder_name)
                new_event.images.append(url)

        db.commit()
        db.refresh(new_event)
        return new_event

    except IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        await utils.delete_folder(event_DIR+"/"+folder_name)        
        raise HTTPException(status_code=500, detail="UNIQUE constraint failed on field")
        
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        await utils.delete_folder(event_DIR+"/"+folder_name)
        raise HTTPException(status_code=500, detail="failed to upload images")

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
    base = db.query(models.Events).filter(models.Events.id == id).first()
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
        event = db.query(models.Events).filter(models.Events.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_event_by_id(id, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))

async def delete_event(id: int, db: Session):
    try:
        event = await read_event_by_id(id, db)
        if event and len(event.images):
            await utils.delete_folder(event_DIR+"/"+event.images[0].folder_name)
            db.delete(event)
            db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()) )

async def add_item_to_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                event.event_items.append(product)
        db.commit()
        db.refresh(event)
        return event
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def remove_item_from_event(id: int, payload: List[int], db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
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

async def add_image_to_event(id: int, images, db: Session):
    event = await read_event_by_id(id, db)
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    urls = []
    try:
        if len(event.images) and await utils.folder_exists(event_DIR+"/"+event.images[0].folder_name):
            new_index = len(os.listdir(event_DIR+"/"+event.images[0].folder_name))            
            image_io = ImageIO(event_DIR+"/"+event.images[0].folder_name)
            for image in images:
                ftype, fext = image.content_type.split('/')
                fn = "img_"+str(new_index+images.index(image)+1)
                image_b = await image.read()
                if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(event_DIR+"/"+event.images[0].folder_name+"/"+fn+"."+fext):
                    new_image_obj = models.EventImages(image_url="events/{folder_name}/{fn}.{fext}".format(folder_name=event.images[0].folder_name, fn=fn, fext=fext), folder_name=event.images[0].folder_name)
                    event.images.append(new_image_obj)         
        else: 
            folder_name = utils.gen_alphanumeric_code_lower(length=15)
            while await utils.folder_exists(event_DIR+"/"+folder_name):
                continue
            if not await folder_io.create(folder_name):
                raise HTTPException(status_code=500, detail="could not create dir for image store")
            image_io = ImageIO(await folder_io._directory())
            for image in images:
                ftype, fext = image.content_type.split('/')
                fn = "img_"+str(images.index(image)+1)
                image_b = await image.read()                
                if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(event_DIR+"/"+folder_name+"/"+fn+"."+fext):
                    new_image_obj = models.EventImages(image_url="events/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext), folder_name=folder_name)
                    event.images.append(new_image_obj)        
        db.commit()
        db.refresh(event)
        return event
        
    except:
        print("{}".format(sys.exc_info()))
        db.rollback()
        raise HTTPException(status_code=500)

async def remove_image_from_event(id, db:Session):
    event_image = db.query(models.EventImages).filter(models.EventImages.id == id).first()
    try: 
        if event_image:
            p_dir, folder_name, image_name = event_image.image_url.split("/")
            if await utils.file_exists(event_DIR+"/"+folder_name+"/"+image_name) and await utils.delete_file(event_DIR+"/"+folder_name+"/"+image_name):
                db.delete(event_image)
                db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()) )