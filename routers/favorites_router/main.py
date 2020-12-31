from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import schemas, crud
from main import get_db
from typing import List

router = APIRouter()

@router.post("/{user_id}/products/{product_id}", description="toggle user favorite products")
async def toggle_user_favorite_product(user_id:int, product_id:int, db:Session=Depends(get_db)):
    return await crud.toggle_user_favorite_product(user_id, product_id, db)

@router.get("/{user_id}", response_model=List[schemas.Product])
async def read_user_favorites(user_id:int, skip:int=0, limit:int=100, search:str=None, value:str=None, db:Session=Depends(get_db)):
    return await crud.read_user_favorites(user_id, skip, limit, search, value, db)