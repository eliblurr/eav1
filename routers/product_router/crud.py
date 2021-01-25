from ..purchase_type_router.crud import read_purchase_type_by_id
from ..weight_unit_router.crud import read_weight_unit_by_id
from ..location_router.crud import read_location_by_id, read_country_by_id, read_sub_country_by_id
from ..currency_router.crud import read_currency_by_id
# from ..category_router.crud import read_category_by_id
from base_classes import ImageIO, FolderIO, ImageFolderIO
from ..category_router.models import Categories
from ..users_router.crud import read_user_by_id
from ..location_router.models import Location, Country, SubCountry
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
    country = await read_country_by_id(payload.country_id, db)
    res = ( country, await read_user_by_id(payload.owner_id, db) )
    if not all(res):
        raise HTTPException(status_code=404, detail='{} not found'.format('country' if not res[0] else 'user'))
    try:
        urls, folder_name = await image_folder_io.create(images, 700, 500)
        new_product = models.Products( **payload.dict(exclude={'category_ids', 'event_ids', 'location_ids', 'payment_info', 'country_id'}),  weight_unit_id=country.weight_unit_id)
        db.add(new_product)
        for purchase_type in payload.payment_info:
            if await read_purchase_type_by_id(purchase_type.purchase_type_id, db):
                payment_info = models.ProductPaymentInfo(**purchase_type.dict(), currency_id=country.currency_id)
                new_product.payment_info.append(payment_info)
        db.flush()
        # append to category
        for id in payload.category_ids:
            category = db.query(Categories).filter(Categories.id==id).first()
            if category:
                new_product.categories.append(category)
        # append to event
        for id in payload.event_ids:
            event = db.query(Events).filter(Events.id == id).first()
            if event:
                new_product.events.append(event)
        # append to location
        locations = db.query(Location).join(SubCountry).join(Country).filter(Country.id==country.id)
        for id in payload.location_ids:
            location = db.query(Location).filter(Location.id == id).first()
            if location in locations.all():
                new_product.locations.append(location) 
        # append images
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

async def read_products(skip, limit, search, value, location_id, sub_country_id, country_id,db: Session): 
    base = db.query(models.Products)
    if country_id and await read_country_by_id(country_id, db):
        base = base.join(Location).join(SubCountry).join(Country).filter(Country.id==country.id)
    elif sub_country_id and await read_sub_country_by_id(sub_country_id, db):
        base = base.join(Location).join(SubCountry).filter(SubCountry.id == sub_country_id)
    elif location_id and await read_location_by_id(location_id, db):
        base = base.join(Location).filter(Location.id == location_id)
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_product_by_id(id: int, db: Session):
    return db.query(models.Products).filter(models.Products.id==id).first()

async def update_product(id: int, payload: schemas.UpdateProduct, db: Session):
    product = await read_product_by_id(id, db)
    if not product:
        raise HTTPException(status_code=404)
    try: 
        if payload.payment_info:
            if payload.payment_info.purchase_type_id and not await read_purchase_type_by_id(payload.payment_info.purchase_type_id, db):
                detail = "purchase type not found"
                raise NotFoundError()
            product.payment_info.filter(models.ProductPaymentInfo.id==payload.payment_info.payment_info_id).update(payload.payment_info.dict(exclude={'payment_info_id','purchase_type_id'}, exclude_unset=True))
        updated = db.query(models.Products).filter(models.Products.id==id).update(payload.dict(exclude={'payment_info'}, exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_product_by_id(id, db)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=detail)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
    
async def delete_product(id: int, db: Session):
    try:
        product = await read_product_by_id(id, db)
        if product:
            if len(product.images):
                await utils.delete_folder(product_DIR+"/"+product.images[0].folder_name)
            db.delete(product)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

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

async def toggle_product_payment_info(id:int, payment_info_id:int, db:Session): 
    try:
        product = await read_product_by_id(id, db)
        payment_info = db.query(models.ProductPaymentInfo).filter(models.ProductPaymentInfo.id==payment_info_id).first()
        test = (product, payment_info)
        if not all(test):
            detail = "product not found" if not test[0] else "payment info not found"
            raise NotFoundError() 
        if payment_info in product.payment_info:
            product.payment_info.remove(payment_info)
        else:
            product.payment_info.append(payment_info)
        db.commit()
        db.refresh(product)
        return product
    except NotFoundError:
        raise HTTPException(status_code=404, detail=detail)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

class NotFoundError(Exception):
    def __init__(self):
        pass
