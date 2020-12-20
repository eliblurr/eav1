from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Product)
async def create_product( payload: schemas.ProductBase, db: Session = Depends(get_db)):
    return await crud.create_product(payload, db)
    
@router.get("/")
async def read_products(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_products(skip,limit,search,value,db)

@router.get("/{id}")
async def read_products(id: int, db: Session = Depends(get_db)):
    return await crud.read_products_by_id(id ,db)

@router.delete('/{id}')
async def delete_product(id: int, db: Session = Depends(get_db)):
    return await crud.delete_product(id, db)



# @router.get("/{id}")
# async def read_item(id: int, db: Session = Depends(get_db)):
#     return await crud.get_item(db, id)
     
# @router.post("/create")
# async def create_item(item:schemas.ItemCreate, db: Session = Depends(get_db)):
#     return await crud.create_item(db, item)

# @router.delete("/delete/{id}")
# async def delete_item(id: int, db: Session = Depends(get_db)):
#     return await crud.delete_item(db, id)

# @router.put("/update/{id}")
# async def update_item(id: int, payload: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return await crud.update_item(db,id,payload)

import os

@router.post("/products/uploadfile/")
async def create_image_and_directory(product_title: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    image = await file.read()
    # ./image/[USER_ID]/[ALBUM_ID]/[PICTURE_ID].[FORMAT]
    os.mkdir('./product_images/{}'.format(product_title))
    with open('./product_images/{}/new_image.png'.format(product_title), 'wb') as new_image:
        new_image.write(image)
    return True

@router.get("/products/image/")
async def get_image_url(db: Session = Depends(get_db)):
    # image = await file.read()
    # os.mkdir('./product_images/{}'.format(product_title))
    # with open('./product_images/{}/new_image.png'.format(product_title), 'wb') as new_image:
    #     new_image.write(image)
    return True

from pydantic import BaseModel
import datetime

# from ..category_router.schemas import CategoryBase
class Category(BaseModel):
    id: int
    title: str
    metatitle: str
    description: str
    # images = relationship('CategoryImages', backref="category", uselist=True, cascade="all, delete")


    date_created: datetime.datetime
    date_modified: datetime.datetime
#     date_created: datetime.datetime
#     date_modified: datetime.datetime
#     images: List

@router.get("/test/{id}")
async def test(id:int, db: Session = Depends(get_db)):
    return await crud.get_prod_category(id, db)
