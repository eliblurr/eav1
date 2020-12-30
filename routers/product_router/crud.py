from ..purchase_type_router.crud import read_purchase_type_by_id
from ..weight_unit_router.crud import read_weight_unit_by_id
from ..location_router.crud import read_location_by_id
from ..currency_router.crud import read_currency_by_id
from helper import ImageIO, FolderIO, ImageFolderIO
from ..category_router.models import Categories
from ..users_router.crud import get_user_by_id
from ..location_router.models import Location
from ..reviews_router.models import Reviews
from fastapi import Depends, HTTPException
from ..events_router.models import Events
from static.main import product_DIR
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import exc
from typing import List
import utils
import sys
import os

folder_io = FolderIO(product_DIR)
image_folder_io = ImageFolderIO(product_DIR, 15, folder_io, 'products')

async def create_product(payload: schemas.CreateProduct, images, db: Session):
    results = (await read_purchase_type_by_id(payload.purchase_type_id, db) is not None, await read_currency_by_id(payload.currency_id, db) is not None, await get_user_by_id(payload.owner_id, db) is not None)
    if all(results):
        pass
    else:
        pass
        # raise HTTPException(status_code=404, detail="{} not found".format('purchase_type' if not(results[0]) else 'currency' if not(results[1]) else 'user'))
    
    results = (not(utils.logical_xor(payload.wholesale_price, payload.wholesale_quantity)), not(utils.logical_xor(payload.weight, payload.weight_unit_id)))
    if all(results):
        pass
    else:
        raise HTTPException(status_code=400)
    
    if bool(payload.weight_unit_id) and await read_weight_unit_by_id(payload.weight_unit_id, db) is None:
        raise HTTPException(status_code=404)

    try:
        urls, folder_name = await image_folder_io.create(images, 700, 500)
        if payload.available_quantity is None:
            payload.available_quantity = payload.initial_quantity
        product_dict = {k:v for (k,v) in payload.dict().items() if k != 'category_ids' and k != 'event_ids' and k != 'location_ids'}
        new_product = models.Products(**product_dict)
        db.add(new_product) 
        db.flush()

        for id in payload.category_ids:
            category = db.query(Categories).filter(Categories.id == id).first()
            if category is not None:
                new_product.categories.append(category)

        for id in payload.event_ids:
            event = db.query(Events).filter(Events.id == id).first()
            if event is not None:
                new_product.events.append(event)

        for id in payload.location_ids:
            location = db.query(Location).filter(Location.id == id).first()
            if location is not None:
                new_product.locations.append(location)     

        for url in urls:
            url = models.ProductImages(image_url=url, folder_name=folder_name)
            new_product.images.append(url)

        db.commit()
        db.refresh(new_product)
        return new_product

    except exc.IntegrityError:
        db.rollback()    
        print("{}".format(sys.exc_info()))        
        raise HTTPException(status_code=409)  
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_products(skip, limit, search, value, location_id, db: Session): 
    base = db.query(models.Products)
    if location_id:
        location = await read_location_by_id(location_id, db)
        if location is None:
            base = db.query(models.Products)
        base = location.location_items
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_product_by_id(id: int, db: Session):
    return db.query(models.Products).filter(models.Products.id == id).first()

async def read_product_review(id: int, skip: int, limit: int, search: str, value: str, db: Session):
    base = await read_product_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    if search and value:
        try:
            base = base.filter(models.Reviews.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.reviews.offset(skip).limit(limit).all()
    return base.reviews.offset(skip).limit(limit).all()

async def update_product(id: int, payload: schemas.UpdateProduct, db: Session):
    if not await read_product_by_id(id, db):
        raise HTTPException(status_code=404)

    payload.purchase_type_id = payload.purchase_type_id if (bool(payload.purchase_type_id) and await read_purchase_type_by_id(payload.purchase_type_id, db) is not None) else None
    payload.currency_id = payload.currency_id if (bool(payload.currency_id) and await read_currency_by_id(payload.currency_id, db) is not None) else None
    payload.weight_unit_id = payload.weight_unit_id if (bool(payload.weight_unit_id) and await read_weight_unit_by_id(payload.weight_unit_id, db) is not None) else None
    payload_dict = {k:v for (k,v) in payload.dict().items() if v is not None}

    try:      
        updated = db.query(models.Products).filter(models.Products.id == id).update(payload_dict)
        db.commit()
        if bool(updated):
            return await read_product_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        db.close()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
    
async def delete_product(id: int, db: Session):
    try:
        product = await read_product_by_id(id, db)
        if product:
            db.delete(product)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_product_image(id: int, images, db: Session):  
    product = await read_product_by_id(id, db)  
    if not product:
        raise HTTPException(status_code=404)
    try:
        urls, folder_name = await image_folder_io.append_image(product, images, 700, 500)
        if urls and folder_name:
            for url in urls:
                url = models.ProductImages(image_url=url, folder_name=folder_name)
                product.images.append(url)
        db.commit()
        db.refresh(product)
        return product
    except:      
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_product_image(id: int, db:Session):
    product_image = db.query(models.ProductImages).filter(models.ProductImages.id == id).first()
    try: 
        if product_image:
            _ , folder_name, image_name = product_image.image_url.split("/")
            if await utils.file_exists(product_DIR+"/"+folder_name+"/"+image_name) and await utils.delete_file(product_DIR+"/"+folder_name+"/"+image_name):
                db.delete(product_image)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)