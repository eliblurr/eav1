from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from . import crud, schemas,models
from typing import List, Optional
from pydantic import UUID4, EmailStr
import jwt
from datetime import timedelta
import sys

from main import get_db, oauth2_scheme
import utils

access_token_expires = timedelta(minutes=30)

router = APIRouter()

# create board
# view board summary
# view board products
# view board by id
# view boards
# update board details
# delete board
# add product to board
# remove product from board
# view user boards

@router.post("/user/{user_id}", status_code=status.HTTP_201_CREATED, description="create new board", response_model = schemas.Board)
async def create_board(payload: schemas.CreateBoard, user_id: int, db: Session = Depends(get_db)):
    return await crud.create_board(payload, user_id, db)

@router.delete("/{id}", description="delete board by board id")
async def delete_board(id: int, db: Session = Depends(get_db)):
    if not await crud.delete_board(id, db):  
        raise HTTPException( status_code=400)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/user/{id}", description="read user boards[General]")
async def read_user_boards(id: int,skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_user_boards(id, skip, limit, search, value, db)

@router.get("/{id}", description="read board by board id")
async def read_board_by_id(id: int, db: Session = Depends(get_db)):
    board = await crud.read_board_by_id(id, db)
    if board is None:
        raise HTTPException(status_code=404)
    return board

@router.get("/{id}/products", description="read board product(s) from existing board by board id")
async def read_board_products(id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await crud.read_board_products(id, skip, limit, db)

@router.patch("/{id}/products", description="add product(s) to existing board")
async def add_product_to_board(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.add_product_to_board(id, payload, db)

@router.delete("/{id}/products", description="remove product(s) from existing board")
async def remove_product_from_board(id: int, payload: List[int], db: Session = Depends(get_db)):
    return await crud.remove_product_from_board(id, payload, db)

@router.patch("/{id}", description="update existing board details")
async def update_board_details(id: int, payload: schemas.UpdateBoard, db: Session = Depends(get_db)):
    return await crud.update_board_details(id, payload, db)

@router.get("/", description="read boards[General]")
async def read_boards(skip: int = 0, limit: int = 100, search:str=None, value:str=None, db: Session = Depends(get_db)):
    return await crud.read_boards(skip, limit, search, value, db)
