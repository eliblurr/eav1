from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from . import models, schemas

async def create_product( payload: schemas.ProductBase, db: Session):
    new_product = models.Products(**payload.dict())
    db.add(new_product)    
    db.commit()
    db.refresh(new_product)
    return new_product

async def read_products(skip, limit, search, value, db: Session):
    base = db.query(models.Products)
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%"))
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

async def read_products_by_id(id, db: Session):
    return db.query(models.Products).filter(models.Products.id == id).first()
    
async def delete_product(id, db: Session):
    product = await read_products_by_id(id, db)
    if not product:
        raise HTTPException(status_code=404)
    db.delete(product)
    db.commit()
    return bool(product)


# async def get_items(db: Session, skip: int = 0, limit: int = 100, search:str=None, value:str=None):
#     base = db.query(models.Item)
#     if search and value:
#         try:
#             base = base.filter(models.Item.__table__.c[search].like("%" + value + "%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def get_item(db: Session, id: int):
#     return db.query(models.Item).filter(models.Item.id == id).first()


# async def delete_item(db: Session, id: int):
#     item = db.query(models.Item).filter(models.Item.id == id).first()
#     if not item:
#         return 'item not found'
#     db.delete(item)
#     db.commit()
#     return 'success'

# async def update_item(db: Session, id: int, payload: schemas.ItemCreate):
#     item = db.query(models.Item).filter(models.Item.id == id).first()
#     if not item:
#         return 'item not found'
#     res = db.query(models.Item).filter(models.Item.id == id).update(payload)
#     db.commit()
#     return res




