from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db
import utils
import sys

router = APIRouter()

@router.post("/", description="create new category", response_model=schemas.Category)
async def create_category(payload=Depends(schemas.CreateCategory.as_form), images: List[UploadFile]=File(...), db: Session=Depends(get_db)):
    return await crud.create_category(payload, images, db)

@router.get("/", description="get/search categories", response_model= List[schemas.Category])
async def read_category(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_category(skip, limit, search, value, db)

@router.get("/{id}", description="get category by id", response_model = schemas.Category)
async def read_category_by_id(id: int, db: Session = Depends(get_db)):
    category = await crud.read_category_by_id(id, db)
    if category is None:
        raise HTTPException(status_code=404)
    return category

@router.get("/{id}/items", description="get/search categories", response_model = schemas.CategoryItems)
async def read_category_products(id: int,skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_category_products(id, skip, limit, search, value, db)

@router.patch("/{id}", description="update category details", response_model = schemas.Category)
async def update_category_details(id: int, payload: schemas.UpdateCategory, db: Session = Depends(get_db)):
    return await crud.update_category(id, payload, db)

@router.delete("/{id}", description="delete category by id")
async def delete_category(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_category(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}/items", description="add product to category with id value", response_model = schemas.Category)
async def add_item_to_category(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_item_to_category(id, payload, db)

@router.delete("/{id}/items", description="remove product to category with id value", response_model = schemas.Category)
async def remove_item_from_category(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_item_from_category(id, payload, db)

@router.patch("/{id}/images", description="add image to category", response_model = schemas.Category)
async def add_image_to_category(id: int, images: List[UploadFile] = File(...),db: Session = Depends(get_db)):
    return await crud.add_image_to_category(id, images, db)

@router.delete("/images/{id}", description="remove image for category")
async def remove_image_from_category(id: int, db: Session = Depends(get_db)):
    if not await crud.remove_image_from_category(id, db):
        raise HTTPException( status_code=500)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

