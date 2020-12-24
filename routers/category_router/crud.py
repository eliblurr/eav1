from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..product_router.crud import read_products_by_id
from ..product_router.models import Products
from fastapi import Depends, HTTPException
from static.main import category_DIR
from helper import ImageIO, FolderIO
from sqlalchemy import update, and_
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from main import get_db
import utils
import sys
import os

folder_io = FolderIO(category_DIR)

async def create_category(payload: schemas.CreateCategory, images, db: Session):
    urls = []
    try:
        folder_name = utils.gen_alphanumeric_code_lower(length=15)
        while await utils.folder_exists(category_DIR+"/"+folder_name):
            continue
        
        if not await folder_io.create(folder_name):
            raise HTTPException(status_code=500)

        image_io = ImageIO(await folder_io._directory())

        for image in images:
            ftype, fext = image.content_type.split('/')
            fn = "img_"+str(images.index(image)+1)
            image_b = await image.read()

            if ftype == 'image':
                await image_io.create_thumbnail(image_b, fn, fext , 600, 200)
                urls.append("categories/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext) )

        new_category = models.Categories(**payload.dict())
        db.add(new_category) 
        db.flush()

        if len(urls):
            for url in urls:
                url = models.CategoryImages(image_url=url, folder_name=folder_name)
                new_category.images.append(url)

        db.commit()
        db.refresh(new_category)
        return new_category

    except IntegrityError:
        db.rollback()      
        print("{}".format(sys.exc_info()))
        await utils.delete_folder(category_DIR+"/"+folder_name)        
        raise HTTPException(status_code=500, detail="UNIQUE constraint failed on field")
        
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        await utils.delete_folder(category_DIR+"/"+folder_name)
        raise HTTPException(status_code=500, detail="failed to upload images")

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
    base = db.query(models.Categories).filter(models.Categories.id == id).first()
    if not base:
        raise HTTPException(status_code=404)
    base = base.category_items
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()
    # db.query(models.Categories).filter(models.Categories.id == id).first().category_items.offset(skip).limit(limit).all()

async def update_category(id: int, payload: schemas.UpdateCategory, db: Session):
    if not await read_category_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        category = db.query(models.Categories).filter(models.Categories.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_category_by_id(id, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail = "unique constraint failed on index")
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return

async def delete_category(id: int, db: Session):
    try:
        category = await read_category_by_id(id, db)
        if category and len(category.images):
            await utils.delete_folder(category_DIR+"/"+category.images[0].folder_name)
            db.delete(category)
            db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()) )

async def add_item_to_category(id: int, payload: List[int], db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
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
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
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

async def add_image_to_category(id: int, images, db: Session):
    category = await read_category_by_id(id, db)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    urls = []
    try:
        if len(category.images) and await utils.folder_exists(category_DIR+"/"+category.images[0].folder_name):
            new_index = len(os.listdir(category_DIR+"/"+category.images[0].folder_name))            
            image_io = ImageIO(category_DIR+"/"+category.images[0].folder_name)
            for image in images:
                ftype, fext = image.content_type.split('/')
                fn = "img_"+str(new_index+images.index(image)+1)
                image_b = await image.read()
                if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(category_DIR+"/"+category.images[0].folder_name+"/"+fn+"."+fext):
                    new_image_obj = models.CategoryImages(image_url="categories/{folder_name}/{fn}.{fext}".format(folder_name=category.images[0].folder_name, fn=fn, fext=fext), folder_name=category.images[0].folder_name)
                    category.images.append(new_image_obj)         
        else: 
            folder_name = utils.gen_alphanumeric_code_lower(length=15)
            while await utils.folder_exists(category_DIR+"/"+folder_name):
                continue
            if not await folder_io.create(folder_name):
                raise HTTPException(status_code=500, detail="could not create dir for image store")
            image_io = ImageIO(await folder_io._directory())
            for image in images:
                ftype, fext = image.content_type.split('/')
                fn = "img_"+str(images.index(image)+1)
                image_b = await image.read()                
                if ftype == 'image' and await image_io.create_thumbnail(image_b, fn, fext , 600, 200) and await utils.file_exists(category_DIR+"/"+folder_name+"/"+fn+"."+fext):
                    new_image_obj = models.CategoryImages(image_url="categories/{folder_name}/{fn}.{fext}".format(folder_name=folder_name, fn=fn, fext=fext), folder_name=folder_name)
                    category.images.append(new_image_obj)        
        db.commit()
        db.refresh(category)
        return category
        
    except:
        print("{}".format(sys.exc_info()))
        db.rollback()
        raise HTTPException(status_code=500)

async def remove_image_from_category(id, db:Session):
    category_image = db.query(models.CategoryImages).filter(models.CategoryImages.id == id).first()
    try: 
        if category_image and await utils.file_exists(category_DIR+"/"+folder_name+"/"+image_name):
            p_dir, folder_name, image_name = category_image.image_url.split("/")
            if await utils.delete_file(category_DIR+"/"+folder_name+"/"+image_name):
                db.delete(category_image)
                db.commit()
        return True
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}".format(sys.exc_info()) )

# 704×480
# 1280×720
# 1920×1080