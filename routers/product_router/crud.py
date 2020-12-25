from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from ..location_router.crud import read_location_by_id

async def create_product( payload: schemas.ProductBase, db: Session):
    new_product = models.Products(**payload.dict())
    db.add(new_product)    
    db.commit()
    db.refresh(new_product)
    return new_product

async def read_products(skip, limit, search, value, location_id, db: Session):
    base = db.query(models.Products)
    if location_id:
        location = read_location_by_id(id, db)
        if not location:
            raise HTTPException(status_code=404)
        base = location.location_items
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


# async def read_event_products(id:int, skip: int, limit: int, search:str, value:str, db: Session):
#     base = db.query(models.Events).filter(models.Events.id == id).first()
#     if not base:
#         raise HTTPException(status_code=404)
#     base = base.event_items
#     if search and value:
#         try:
#             base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

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

# async def get_prod_category()
async def get_prod_category(id, db: Session):
    item = db.query(models.Products).filter(models.Products.id == id).first()
    # for item in item.category:
    #     print(item)
    # print(item.category.all())
    # print(dir(item.category))
    return item.category.all()

# Update
# purchase_type_id: Optional[int]
#     weight_unit_id: Optional[int]
#     owner_id: Optional[int]
#     currency_id: Optional[int]

# create
# update
# read + read by location
# read by id
# read by location
# delete
# filter


# base = db.query(models.Events).filter(models.Events.id == id).first()
#     if not base:
#         raise HTTPException(status_code=404)
#     base = base.event_items
#     if search and value:
#         try:
#             base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

    # db.query(models.Categories).filter(models.Categories.id == id).first().category_items.offset(skip).limit(limit).all()



