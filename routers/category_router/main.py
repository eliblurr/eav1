from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from . import crud, schemas
from typing import List
from main import get_db
import utils
import sys

router = APIRouter()

@router.post("/", description="create new category", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
async def create_category(payload=Depends(schemas.CreateCategory.as_form), images: List[UploadFile]=File(...), db: Session=Depends(get_db)):
    return await crud.create_category(payload, images, db)

@router.get("/", description="read categories", response_model= List[schemas.Category])
async def read_category(skip: int = 0, limit: int = 100, search:str = None, value:str = None, db: Session = Depends(get_db)):
    return await crud.read_category(skip, limit, search, value, db)

@router.get("/{id}", description="read category by id", response_model=schemas.Category)
async def read_category_by_id(id: int, db: Session=Depends(get_db)):
    category = await crud.read_category_by_id(id, db)
    if category is None:
        raise HTTPException(status_code=404)
    return category

@router.get("/{id}/products", description="read category products", response_model=List[schemas.Product])
async def read_category_products(id: int, skip: int=0, limit: int=100, search: str=None, value: str=None, db: Session=Depends(get_db)):
    return await crud.read_category_products(id, skip, limit, search, value, db)

@router.patch("/{id}", description="update category", response_model=schemas.Category, status_code=status.HTTP_202_ACCEPTED)
async def update_category(id: int, payload: schemas.UpdateCategory, db: Session=Depends(get_db)):
    return await crud.update_category(id, payload, db)

@router.patch("/{id}/images", description="add image to category", response_model=schemas.Category, status_code=status.HTTP_202_ACCEPTED)
async def add_category_image(id: int, images: List[UploadFile]=File(...), db: Session=Depends(get_db)):
    return await crud.add_category_image(id, images, db)

@router.patch("/{id}/products", description="add product to category", response_model = schemas.Category, status_code=status.HTTP_202_ACCEPTED)
async def add_product_to_category(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_product_to_category(id, payload, db)

@router.delete("/{id}", description="delete category", status_code=status.HTTP_202_ACCEPTED)
async def delete_category(id: int, db: Session=Depends(get_db)):
    return await crud.delete_category(id, db)

@router.delete("/images/{id}", description="delete category image", status_code=status.HTTP_202_ACCEPTED)
async def remove_category_image(id: int, db:Session=Depends(get_db)):
    return await crud.remove_category_image(id, db)

@router.delete("/products/{id}", description="remove product from category", status_code=status.HTTP_202_ACCEPTED)
async def remove_product_from_category(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_product_from_category(id, payload, db)