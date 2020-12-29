from ..purchase_type_router.crud import read_purchase_type_by_id
from ..location_router.crud import read_location_by_id
from ..currency_router.crud import read_currency_by_id
from helper import ImageIO, FolderIO, ImageFolderIO
from ..category_router.models import Categories
from ..users_router.crud import get_user_by_id
from ..location_router.models import Location
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

    
# async def read_products(skip, limit, search, value, location_id, db: Session):
#     base = db.query(models.Products)
#     if location_id:
#         location = read_location_by_id(id, db)
#         if not location:
#             raise HTTPException(status_code=404)
#         base = location.location_items
#     if search and value:
#         try:
#             base = base.filter(models.Products.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def read_products_by_id(id, db: Session):
#     return db.query(models.Products).filter(models.Products.id == id).first()
    
# async def delete_product(id, db: Session):
#     product = await read_products_by_id(id, db)
#     if not product:
#         raise HTTPException(status_code=404)
#     db.delete(product)
#     db.commit()
#     return bool(product)


# async def read_event_products(id:int, skip: int, limit: int, search:str, value:str, db: Session):
#     base = db.query(models.Events).filter(models.Events.id == id).first()
#     if not base:
#         raise HTTPException(status_code=404)
#     base = base.event_items
#     if search and value:
#         try:
#             base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def get_items(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
#     base = db.query(models.Item)
#     if search and value:
#         try:
#             base = base.filter(models.Item.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def get_item(db: Session, id: int):
#     return db.query(models.Item).filter(models.Item.id == id).first()


# async def delete_item(db: Session, id: int):
#     item = db.query(models.Item).filter(models.Item.id == id).first()
#     if not item:
#         return 'item not found'
#     db.delete(item)
#     db.commit()
#     return 'success'

# async def update_item(db: Session, id: int, payload: schemas.ItemCreate):
#     item = db.query(models.Item).filter(models.Item.id == id).first()
#     if not item:
#         return 'item not found'
#     res = db.query(models.Item).filter(models.Item.id == id).update(payload)
#     db.commit()
#     return res

# async def get_prod_category()
# async def get_prod_category(id, db: Session):
    # item = db.query(models.Products).filter(models.Products.id == id).first()
    # for item in item.category:
    #     print(item)
    # print(item.category.all())
    # print(dir(item.category))
    # return item.category.all()

# Update
# purchase_type_id: Optional[int]
#     weight_unit_id: Optional[int]
#     owner_id: Optional[int]
#     currency_id: Optional[int]

# create
# update
# read + read by location
# read by id
# read by location
# delete
# filter and sort/group
# get product reviews
# get product owner

# base = db.query(models.Events).filter(models.Events.id == id).first()
#     if not base:
#         raise HTTPException(status_code=404)
#     base = base.event_items
#     if search and value:
#         try:
#             base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

    # db.query(models.Categories).filter(models.Categories.id == id).first().category_items.offset(skip).limit(limit).all()



