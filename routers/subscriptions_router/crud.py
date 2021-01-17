# from sqlalchemy.orm import Session
# from fastapi import Depends, HTTPException
# from sqlalchemy import update, and_
# # import sys

# from main import get_db

# import utils

# import sys

# from . import models, schemas

# from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# from ..priorities_router.crud import read_priority_by_id


# async def create_subscription(payload: schemas.SubscriptionCreate, db: Session):
#     subscription_type = await read_subscription_type_by_id(payload.subscription_type_id, db)
#     if not subscription_type:
#         raise HTTPException(status_code=404, detail = "subscription type not found")

#     if subscription_type.title == 'periodic' and payload.duration is None:
#         raise HTTPException(status_code = 418, detail = "duration cannot be empty for periodic subscriptions")

#     if subscription_type.title == 'periodic' and payload.duration < 1:
#         raise HTTPException(status_code=418, detail="duration should be greater than 0")
    
#     priority = await read_priority_by_id(payload.priority_id, db)
#     if not priority:
#         raise HTTPException(status_code=404, detail = "priority not found")

#     try:
#         new_subscription = models.Subscriptions(**payload.dict(exclude_unset=True), priority=priority, subscription_type=subscription_type)
#         db.add(new_subscription)
#         db.commit()
#         db.refresh(new_subscription)
#         return new_subscription

#     except IntegrityError as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="value should be unique")
#     except:
#         db.rollback()

# async def delete_subscription(id: int, db: Session):
#     try:
#         subscription = await read_subscription_by_id(id, db)
#         if subscription:
#             db.delete(subscription)
#         db.commit()
#         return True
#     except:
#         db.rollback()

# async def update_subscription(id: int, payload: schemas.SubscriptionUpdate, db: Session):
#     if payload.subscription_type_id:
#         subscription_type = await read_subscription_type_by_id(payload.subscription_type_id, db)
        
#         if subscription_type is None:
#             raise HTTPException(status_code=404, detail = "subscription type not found")

#         if subscription_type.title == 'periodic' and payload.duration is None:
#             raise HTTPException(status_code = 418, detail = "duration cannot be empty for periodic subscriptions")

#         if subscription_type.title == 'periodic' and payload.duration < 1:
#             raise HTTPException(status_code=418, detail="duration should be greater than 0")
    
#     if payload.priority_id is not None:
#         if not await read_priority_by_id(payload.priority_id, db):
#             raise HTTPException(status_code=404, detail = "priority not found")
    
#     if not await read_subscription_by_id(id, db):
#         raise HTTPException(status_code=404, detail = "subscription with {id} not found".format(id=id))

#     try:

#         db.query(models.Subscriptions).filter(models.Subscriptions.id == id).update(payload.dict(exclude_unset=True))
#         db.commit()
#         return await read_subscription_by_id(id, db)

#     except:
#         db.rollback()

# async def read_subscription(skip: int, limit: int, search:str, value:str, db: Session):
#     base = db.query(models.Subscriptions)
#     if search and value:
#         try:
#             base = base.filter(models.Subscriptions.__table__.c[search].like("%"+ value +"%"))
#         except KeyError:
#             return base.offset(skip).limit(limit).all()
#     return base.offset(skip).limit(limit).all()

# async def read_subscription_by_id(id: int, db: Session):
#     return db.query(models.Subscriptions).filter(models.Subscriptions.id == id).first()


# async def read_subscription_type_by_id(id, db):
#     return db.query(models.SubscriptionType).filter(models.SubscriptionType.id == id).first()