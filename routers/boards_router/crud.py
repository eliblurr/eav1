from ..product_router.crud import read_product_by_id
from ..auth_router.crud import read_user_by_id
from ..auth_router import models as user_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
from sqlalchemy import exc
from typing import List
import sys

async def create_board(payload: schemas.CreateBoard, db: Session):
    if await read_user_by_id(payload.user_id, db) is None:
        raise HTTPException(status_code=404, detail="user not found")
    payload_cp = payload.dict().copy()
    del payload_cp["product_ids"]
    try:  
        new_board = models.Boards(**payload_cp)
        db.add(new_board) 
        db.flush()
        for id in payload.product_ids:
            product = await read_product_by_id(id, db)
            if product:
                new_board.board_items.append(product)
        db.commit()
        db.refresh(new_board)
        return new_board
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_boards(id:int, skip: int, limit: int, search:str, value:str, db: Session):
    user = await read_user_by_id(id, db)
    if user is None:
        raise HTTPException(status_code=404)
    base = user.boards
    if search and value:
        try:
            base = base.filter(models.Boards.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_board_by_id(id: int, db: Session):
    return db.query(models.Boards).filter(models.Boards.id == id).first()

async def read_board_products(id:int, skip:int, limit:int, search:str, value:str, db: Session):
    base = await read_board_by_id(id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.board_items
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def update_board(id: int, payload: schemas.UpdateBoard, db: Session):
    if not await read_board_by_id(id, db):
        raise HTTPException(status_code=404)
    try:
        updated = db.query(models.Boards).filter(models.Boards.id == id).update(payload.dict(exclude_unset=True))
        db.commit()
        if bool(updated):
            return await read_board_by_id(id, db)
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def delete_board(ids: List[int], db: Session):
    try:
        for id in ids:
            board = await read_board_by_id(id, db)
            if board:
                db.delete(board)
        db.commit()
        return True
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def add_product_to_board(id: int, payload: List[int], db: Session):
    board = await read_board_by_id(id, db)
    if not board:
        raise HTTPException(status_code=404)
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product and (product not in board.board_items):
                board.board_items.append(product)
        db.commit()
        db.refresh(board)
        return board
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def remove_product_from_board(id:int, payload: List[int], db:Session):
    board = await read_board_by_id(id,db)
    if not board:
        raise HTTPException(status_code=404)
    try:
        for id in payload:
            product = await read_product_by_id(id, db)
            if product:
                board.board_items.remove(product)
        db.commit()
        db.refresh(board)
        return board
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)