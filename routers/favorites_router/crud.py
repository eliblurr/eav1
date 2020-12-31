from ..product_router.crud import read_product_by_id
from ..auth_router.crud import read_user_by_id
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from . import models
import sys

async def toggle_user_favorite_product(user_id:int, product_id:int, db:Session):
    try:
        user = await read_user_by_id(user_id, db)
        product = await read_product_by_id(product_id, db)
        res = (user is not None, product is not None)
        if all(res):
            pass
        else:
            raise HTTPException(status_code=404, detail= "{} not found".format('user' if not(res[0]) else 'product'))
        if product in user.favorites:
            user.favorites.remove(product)
            operation = 'removed'
        else:
            user.favorites.append(product)
            operation = 'added'
        db.commit()
        return True, operation
    except exc.IntegrityError:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=409)
    except:
        db.rollback()
        print("{}".format(sys.exc_info()))
        raise HTTPException(status_code=500)

async def read_user_favorites(user_id:int, skip:int, limit:int, search:str, value:str, db:Session):
    base = await read_user_by_id(user_id, db)
    if not base:
        raise HTTPException(status_code=404)
    base = base.favorites
    if search and value:
        try:
            base = base.filter(models.Products.__table__.c[search].like("%" + value + "%")) 
        except KeyError:
            return base.offset(skip).limit(limit).all()
    return base.offset(skip).limit(limit).all()

        

