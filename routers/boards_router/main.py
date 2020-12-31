from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List
from main import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, description="create new board", response_model=schemas.Board)
async def create_board(payload: schemas.CreateBoard, db: Session=Depends(get_db)):
    return await crud.create_board(payload, db)

@router.get("/users/{id}", description="read user boards", response_model=List[schemas.Board])
async def read_boards(id:int, skip:int=0, limit:int=100, search:str=None, value:str=None, db:Session=Depends(get_db)):
    return await crud.read_boards(id, skip, limit, search, value, db)

@router.get("/{id}", description="read board by id", response_model=schemas.Board)
async def read_board_by_id(id:int, db:Session=Depends(get_db)):
    board = await crud.read_board_by_id(id, db)
    if board is None:
        raise HTTPException(status_code=404)
    return board

@router.get("/{id}/products", description="read board products", response_model=List[schemas.Product])
async def read_board_products(id:int, skip:int=0, limit:int=100, search:str=None, value:str=None, db:Session=Depends(get_db)):
    return await crud.read_board_products(id, skip, limit, search, value, db)

@router.patch("/{id}", description="update board details", response_model=schemas.Board, status_code=status.HTTP_202_ACCEPTED)
async def update_board(id:int, payload:schemas.UpdateBoard, db:Session=Depends(get_db)):
    return await crud.update_board(id, payload, db)

@router.patch("/{id}/products", description="add product(s) to board", response_model=schemas.Board, status_code=status.HTTP_202_ACCEPTED)
async def add_product_to_board(id:int, payload:List[int], db:Session=Depends(get_db)):
    return await crud.add_product_to_board(id, payload, db)

@router.delete("/", description="delete board(s) by board id", status_code=status.HTTP_202_ACCEPTED)
async def delete_board(ids:List[int], db:Session=Depends(get_db)):
    return await crud.delete_board(ids, db)

@router.delete("/{id}/products", description="remove product(s) from board", status_code=status.HTTP_202_ACCEPTED)
async def remove_product_from_board(id:int, payload: List[int], db:Session=Depends(get_db)):
    return await crud.remove_product_from_board(id, payload, db)
