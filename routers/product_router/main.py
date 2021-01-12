from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, schemas
from main import get_db

router = APIRouter()

@router.post("/", description="create new product", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
async def create_product(payload:schemas.CreateProduct, db: Session = Depends(get_db)):
    pass
    # return await crud.create_product(payload, images, db)

# @router.post("/", description="create new product", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
# async def create_product(payload = Depends(schemas.CreateProduct.as_form), images: List[UploadFile]=File(...), db: Session = Depends(get_db)):
#     return await crud.create_product(payload, images, db)

# @router.get("/", description="read products", response_model=List[schemas.Product])
# async def read_products(location_id:int=0, skip: int=0, limit: int=100, search:str=None, value:str=None, db: Session=Depends(get_db)):
#     return await crud.read_products(skip, limit, search, value, location_id, db)

# @router.get("/{id}", description="read product by id", response_model=schemas.Product)
# async def read_product_by_id(id: int, db: Session=Depends(get_db)):
#     product = await crud.read_product_by_id(id, db)
#     if product is None:
#         raise HTTPException(status_code=404)
#     return product

# @router.get("/{id}/reviews", description="read product reviews", response_model=List[schemas.Review])
# async def read_product_review(id: int, skip: int=0, limit: int=100, search: str=None, value: str=None, db: Session=Depends(get_db)):
#     return await crud.read_product_review(id, skip, limit, search, value, db)

# @router.patch("/{id}", description="update product", response_model=schemas.Product, status_code=status.HTTP_202_ACCEPTED)
# async def update_product(id: int, payload: schemas.UpdateProduct, db: Session=Depends(get_db)):
#     return await crud.update_product(id, payload, db)

# @router.patch("/{id}/images", description="add image to product", response_model=schemas.Product, status_code=status.HTTP_202_ACCEPTED)
# async def add_product_image(id: int, images: List[UploadFile]=File(...), db: Session=Depends(get_db)): 
#     return await crud.add_product_image(id, images, db)

# @router.delete("/{id}", description="delete product", status_code=status.HTTP_202_ACCEPTED)
# async def delete_product(id: int, db: Session=Depends(get_db)):
#     return await crud.delete_product(id, db)

# @router.delete("/images/{id}", description="delete product image", status_code=status.HTTP_202_ACCEPTED )
# async def remove_product_image(id: int, db:Session=Depends(get_db)):
#     return await crud.remove_product_image(id, db)