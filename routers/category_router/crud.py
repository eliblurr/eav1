from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..product_router.crud import read_products_by_id
from fastapi import Depends, HTTPException
from static.main import category_DIR
from sqlalchemy import update, and_
from sqlalchemy.orm import Session
from . import models, schemas
from helper import ImageIO, FolderIO
from typing import List
from main import get_db
import utils
import sys

folder_io = FolderIO(category_DIR)

async def create_category(payload: schemas.CreateCategory, images, db: Session):
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
                await image_io.create_thumbnail(image_b, fn, fext , 200, 200)
    
            # print(fn)
            # print(ftype)

            # print(type(images.index(image)))
            # print(images.index(image)+1)
            # print(type(await image.read()))
        
            
            # print(fn)
            # print(fext)

        
        # print(type(await file.read()))
        # im = Image.open(file)
        # print(im.format, im.size, im.mode)
        # im.show()
        # return {"filename": file.filename}
        
        # print(category_DIR)
        # print(category_folder)
    except:
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="failed to upload images")

    

# async def create_category(payload: schemas.CreateCategory, images, db: Session):

#     urls = []

#     try:
#         for file in images:
#             image = await file.read()
#             image_id = utils.gen_alphanumeric_code_lower(length=20)
#             _type = file.content_type.split('/')

#             image_url = '/c1a43tnrz5phmwh3/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )
            
#             if not _type[0] == 'image':
#                 continue

#             if await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), image):
#                 urls.append(image_url)
    
#     except:
#         raise HTTPException(status_code=500, detail="failed to upload images")

#     try:  
#         new_category = models.Categories(**payload.dict())
#         db.add(new_category) 
#         db.flush()
        
#         if len(urls):
#             for url in urls:
#                 url = models.CategoryImages(image_url='{static_DIR}{url}'.format(static_DIR=static_DIR,url=url))
#                 new_category.images.append(url)

#         db.commit()
#         db.refresh(new_category)
#         return new_category

#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

# async def delete_category(id: int, db: Session):
#     try:
#         category = await read_category_by_id(id, db)
#         if category:
#             for image in category.images:
#                 utils.delete_file(image.image_url)
#             db.delete(category)
#             db.commit()
#         return True

#     except:
#         print("{}".format(sys.exc_info()))
#         raise HTTPException(status_code=500)

# async def add_item_to_category(id: int, payload: List[int], db: Session):
#     category = await read_category_by_id(id,db)
#     if not category:
#         raise HTTPException(status_code=404, detail="could not find category")
#     try:
#         for id in payload:
#             product = await read_products_by_id(id, db)
#             if product:
#                 category.category_items.append(product)

#         db.commit()
#         db.refresh(category)
#         return category
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500)

# async def remove_item_from_category(id: int, payload: List[int], db: Session):
#     category = await read_category_by_id(id,db)
#     if not category:
#         raise HTTPException(status_code=404, detail="could not find category")
#     try:
#         for id in payload:
#             product = await read_products_by_id(id, db)
#             if product:
#                 category.category_items.remove(product)

#         db.commit()
#         db.refresh(category)
#         return category
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500)

# async def add_image_to_category(id: int, image, db: Session):
#     category = await read_category_by_id(id,db)
#     if not category:
#         raise HTTPException(status_code=404, detail="could not find category")

#     try:
#         _image = await image.read()
#         image_id = utils.gen_alphanumeric_code_lower(length=20)
#         _type = image.content_type.split('/')
#         image_url = '/c1a43tnrz5phmwh3/{image_id}.{image_format}'.format(image_id=image_id, image_format=_type[1] )
            
#         if not _type[0] == 'image':
#             raise HTTPException(status_code=422)

#         if not await utils.create_file('{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url), _image):
#             raise HTTPException(status_code=500, detail="failed to upload image")    
#     except:
#         raise HTTPException(status_code=500, detail="failed to upload images")

#     try:
#         url = models.CategoryImages(image_url='{static_DIR}{image_url}'.format(static_DIR=static_DIR,image_url=image_url))
#         category.images.append(url)
#         db.commit()
#         db.refresh(category)
#         return category
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500)

# async def update_category_details(id: int, payload: schemas.UpdateCategory, db: Session):
#     category = await read_category_by_id(id, db)
#     if not category:
#         raise HTTPException(status_code=404)

#     try:
#         db.query(models.Categories).filter(models.Categories.id == id).update(payload.dict(exclude_unset=True))
#         db.commit()
#         return await read_category_by_id(id, db)

#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="IntegrityError: UNIQUE constraint failed")
        
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500)

# async def read_category(skip: int, limit: int, search:str, value:str, db: Session):
#     base = db.query(models.Categories)
#     if search and value:
#         try:
#             base = base.filter(models.Categories.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def read_category_by_id(id: int, db: Session):
#     return db.query(models.Categories).filter(models.Categories.id == id).first()

# async def remove_image_from_category(id, image_id, db:Session):
#     category = await read_category_by_id(id, db)
#     if category is None:
#         raise HTTPException(status_code=404)
    
#     image = db.query(models.CategoryImages).filter(and_(
#         models.CategoryImages.id == image_id,
#         models.CategoryImages.category_id == id
#     )).first()
#     if image is None:
#         raise HTTPException(status_code=404)

#     try:
#         utils.delete_file('{image_url}'.format(image_url=image.image_url))
#         db.delete(image)
#         db.commit()
#     except:
#         db.rollback()
#         raise HTTPException(status_code=500)

#     db.refresh(category)
#     return category

# async def read_category_products(id: int, skip: int, limit: int, db: Session):
#     if not await read_category_by_id(id, db):
#         raise HTTPException(status_code=404)
#     return db.query(models.Categories).filter(models.Categories.id == id).first().category_items.offset(skip).limit(limit).all()
    

# from fastapi import FastAPI, File, UploadFile
# from PIL import Image
# from io import BytesIO
# import sys
# import os

# @api.post("/files/")
# async def create_file(file: bytes = File(...)):
#     print(type(file))
#     im = Image.open("./test.jpg")
#     print(type(im))
#     print(im.format, im.size, im.mode)
#     im.show()

#     im = Image.open(BytesIO(file))
#     print(im.format, im.size, im.mode)
#     im.show()

#     f, e = os.path.splitext(file)

#     print(type(im))
#     print(f)
#     print(e)


    # stream = BytesIO(LEFT_THUMB)
    # print(dir(BytesIO))

    
    # image = Image.open(stream).convert("RGBA")
    # stream.close()
    # image.show()
    # return {"file_size": len(file)}

# @api.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):

    # print(type(await file.read()))
    # im = Image.open(file)
    # print(im.format, im.size, im.mode)
    # im.show()
    # return {"filename": file.filename}

