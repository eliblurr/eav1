from ..product_router.crud import read_product_by_id
from helper import FolderIO, ImageFolderIO
from static.main import category_DIR
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
from typing import List
import utils
import sys

folder_io = FolderIO(category_DIR)
image_folder_io = ImageFolderIO(category_DIR, 15, folder_io, 'categories')

async def create_category(payload: schemas.CreateCategory, images, db: Session):
    try:
        urls, folder_name = await image_folder_io.create(images, 700, 500)
        new_category = models.Categories(**payload.dict())
        db.add(new_category) 
        db.flush()
        for url in urls:
            url = models.CategoryImages(image_url=url, folder_name=folder_name)
            new_category.images.append(url)
        db.commit()
        db.refresh(new_category)
        return new_category
    except exc.IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
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

async def read_category_products(id:int, skip: int, limit: int, search:str, value:str, db: Session):
    base = await read_category_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.category_items
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def update_category(id: int, payload: schemas.UpdateCategory, db: Session):
    if not await read_category_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Categories).filter(models.Categories.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_category_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_category(id: int, db: Session):
    try:
        category = await read_category_by_id(id, db)
        if category:
            db.delete(category)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_category_image(id: int, images, db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    try:
        urls, folder_name = await image_folder_io.append_image(category, images, 700, 500)
        if urls and folder_name:
            for url in urls:
                url = models.CategoryImages(image_url=url, folder_name=folder_name)
                category.images.append(url)
        db.commit()
        db.refresh(category)
        return category
    except:      
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_category_image(id, db:Session):
    category_image = db.query(models.CategoryImages).filter(models.CategoryImages.id == id).first()
    try: 
        if category_image:
            _ , folder_name, image_name = category_image.image_url.split("/")
            if await utils.file_exists(category_DIR+"/"+folder_name+"/"+image_name) and await utils.delete_file(category_DIR+"/"+folder_name+"/"+image_name):
                db.delete(category_image)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)
    
async def add_product_to_category(id: int, payload: List[int], db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404)
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product and (product not in category.category_items): #check if prod is alrea
                category.category_items.append(product)
            else:
                pass
        db.commit()
        db.refresh(category)
        return category
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409) #product already exists for 
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_product_from_category(id: int, payload: List[int], db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product:
                category.category_items.remove(product)
        db.commit()
        db.refresh(category)
        return category
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)