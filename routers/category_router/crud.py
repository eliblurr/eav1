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
from static.main import static_DIR

async def create_category(payload: schemas.CreateCategory, images, db: Session):

    urls = []

    try:
        for file in images:
            image = await file.read()
            image_id = utils.gen_alphanumeric_code_lower(length=20)
            _type = file.content_type.split('/')

            image_url = '/c1a43tnrz5phmwh3/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )
            
            if not _type[0] == 'image':
                continue

            if await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), image):
                urls.append(image_url)
    
    except:
        raise HTTPException(status_code=500, detail="failed to upload images")

    try:  
        new_category = models.Categories(**payload.dict())
        db.add(new_category) 
        db.flush()
        
        if len(urls):
            for url in urls:
                url = models.CategoryImages(image_url='{static_DIR}{url}'.format(static_DIR=static_DIR,url=url))
                new_category.images.append(url)

        db.commit()
        db.refresh(new_category)
        return new_category

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def delete_category(id: int, db: Session):
    try:
        category = await read_category_by_id(id, db)
        if category:
            for image in category.images:
                utils.delete_file(image.image_url)
            db.delete(category)
            db.commit()
        return True

    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_item_to_category(id: int, payload: List[int], db: Session):
    category = await read_category_by_id(id,db)
    if not category:
        raise HTTPException(status_code=404, detail="could not find category")
    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                category.category_items.append(product)

        db.commit()
        db.refresh(category)
        return category
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def remove_item_from_category(id: int, payload: List[int], db: Session):
    category = await read_category_by_id(id,db)
    if not category:
        raise HTTPException(status_code=404, detail="could not find category")
    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                category.category_items.remove(product)

        db.commit()
        db.refresh(category)
        return category
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def add_image_to_category(id: int, image, db: Session):
    category = await read_category_by_id(id,db)
    if not category:
        raise HTTPException(status_code=404, detail="could not find category")

    try:
        _image = await image.read()
        image_id = utils.gen_alphanumeric_code_lower(length=20)
        _type = image.content_type.split('/')
        image_url = '/c1a43tnrz5phmwh3/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )
            
        if not _type[0] == 'image':
            raise HTTPException(status_code=422)

        if not await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), _image):
            raise HTTPException(status_code=500, detail="failed to upload image")    
    except:
        raise HTTPException(status_code=500, detail="failed to upload images")

    try:
        url = models.CategoryImages(image_url='{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url))
        category.images.append(url)
        db.commit()
        db.refresh(category)
        return category
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def update_category_details(id: int, payload: schemas.UpdateCategory, db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404)

    try:
        db.query(models.Categories).filter(models.Categories.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_category_by_id(id, db)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def read_category(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Categories)
    if search and value:
        try:
            base = base.filter(models.Categories.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_category_by_id(id: int, db: Session):
    return db.query(models.Categories).filter(models.Categories.id == id).first()

async def remove_image_from_category(id, image_id, db:Session):
    category = await read_category_by_id(id, db)
    if category is None:
        raise HTTPException(status_code=404)
    
    image = db.query(models.CategoryImages).filter(and_(
        models.CategoryImages.id == image_id,
        models.CategoryImages.category_id == id
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

    db.refresh(category)
    return category

async def read_category_products(id: int, skip: int, limit: int, db: Session):
    if not await read_category_by_id(id, db):
        raise HTTPException(status_code=404)
    return db.query(models.Categories).filter(models.Categories.id == id).first().category_items.offset(skip).limit(limit).all()
    