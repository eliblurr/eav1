from fastapi import APIRouter, Depends, HTTPException, status
from . import crud, schemas, models
from sqlalchemy.orm import Session
from main import get_db
from typing import List

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new T&C block", response_model = schemas.TC)
async def create_tC_blocks(payload: schemas.CreateTC, db: Session = Depends(get_db)):
    return await crud.create_tC_blocks(payload, db)

@router.patch("/{id}", description="update tC block",response_model = schemas.TC)
async def update_tC_blocks(id:int, payload: schemas.UpdateTC, db: Session = Depends(get_db)):
    return await crud.update_tC_blocks(id, payload, db)

@router.delete("/", description="delete tC block(s)", status_code=status.HTTP_202_ACCEPTED)
async def delete_tC_block(ids: List[int], db: Session = Depends(get_db)):
    return await crud.delete_tC_block(ids, db)
       
@router.get("/", description="read TC", response_model = List[schemas.TC])
async def read_tC_blocks(skip:int=0, limit:int=100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_tC_blocks(skip, limit, search, value, db)

@router.get("/{id}", description="read TC by id", response_model = schemas.TC)
async def read_tC_block_by_id(id: int, db: Session = Depends(get_db)):
    t_c = await crud.read_tC_block_by_id(id, db)
    if t_c is None:
        raise HTTPException(status_code=404)
    return t_c