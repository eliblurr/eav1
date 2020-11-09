from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sqlalchemy import update, and_
from typing import List

from main import get_db

import utils

import sys

from . import models, schemas

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..product_router.crud import read_products_by_id
from ..auth_router.crud import get_user_by_id
from ..auth_router import models as user_model


async def create_board(payload: schemas.CreateBoard, user_id: int, db: Session):
    owner = await get_user_by_id(user_id, db)
    if owner is None:
        raise HTTPException(status_code=404, detail="could not find user with ID")

    _copy_payload = payload.dict().copy()
    del _copy_payload["board_items_id"]

    try:  
        new_board = models.Boards(**_copy_payload,user=owner)
        db.add(new_board) 
        db.flush()
        
        if len(payload.board_items_id):
            for id in payload.board_items_id:
                product = await read_products_by_id(id, db)
                if product:
                    new_board.board_items.append(product)

        db.commit()
        db.refresh(new_board)
        return new_board

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="UNIQUE constraint failed")

    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def delete_board(id: int, db: Session):
    try:
        board = await read_board_by_id(id,db)
        if board:
            db.delete(board)
        db.commit()
        return True
    except:
        db.rollback()
        # print("{}".format(sys.exc_info()))

async def read_user_boards(id:int,skip: int, limit: int, search:str, value:str, db: Session):
    user = await get_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404)

    base = db.query(user_model.User).filter(user_model.User.id == id).first().boards

    if search and value:
        try:
            base = db.query(user_model.User).filter(user_model.User.id == id).first().boards.filter(models.Boards.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    
    return base.offset(skip).limit(limit).all()

async def read_boards(skip: int, limit: int, search:str, value:str, db: Session):
    base = db.query(models.Boards)
    if search and value:
        try:
            base = base.filter(models.Boards.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_board_by_id(id: int, db: Session):
    return db.query(models.Boards).filter(models.Boards.id == id).first()

async def add_product_to_board(id: int, payload: List[int], db: Session):
    board = await read_board_by_id(id,db)
    if not board:
        raise HTTPException(status_code=404, detail="could not find board")

    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                board.board_items.append(product)

        db.commit()
        db.refresh(board)
        return board
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="product already in board")
    
    except:
        db.rollback()
    # sqlalchemy.exc.IntegrityError when product is already in board

async def remove_product_from_board(id: int, payload: List[int], db: Session):
    board = await read_board_by_id(id,db)
    if not board:
        raise HTTPException(status_code=404, detail="could not find board")

    try:
        for id in payload:
            product = await read_products_by_id(id, db)
            if product:
                board.board_items.remove(product)
        db.commit()
        db.refresh(board)
        return board
    
    except:
        db.rollback()
        raise HTTPException(status_code=500)

async def update_board_details(id: int, payload: schemas.UpdateBoard, db: Session):
    board = await read_board_by_id(id, db)
    if not board:
        raise HTTPException(status_code=404)
    
    try:
        db.query(models.Boards).filter(models.Boards.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        return await read_board_by_id(id, db)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unique constraint failed")
    
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail='something went wrong')

async def read_board_products(id: int, skip, limit, db: Session):
    if not await read_board_by_id(id, db):
        raise HTTPException(status_code=404)
    return db.query(models.Boards).filter(models.Boards.id == id).first().board_items.offset(skip).limit(limit).all()

# async def read_boards_summary(skip: int, limit: int, search:str, value:str, db: Session):
#     base = db.query(models.Boards)
#     if search and value:
#         try:
#             base = base.filter(models.Boards.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()