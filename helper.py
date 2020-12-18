from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import and_
import sys

class CRUD:
    def __init__(self,  model, db):
        self.db = db
        self.model = model
    
    async def read(self, search:str = None, value:str = None, skip: int=0, limit: int=100 ):
        base = self.db.query(self.model)
        if search and value:
            try:
                base = base.filter(self.model.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.all()
        return base.all()
    
    async def read_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).first()

    async def update(self, id, payload):
        if not await self.read_about_us_by_id(id, self.db):
            raise HTTPException(status_code=404)
        
        try:
            self.db.query(self.model).filter(self.model.id == id).update(payload.dict(exclude_unset=True))
            self.db.commit()
            return await self.read_about_us_by_id(id, self.db)
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=422, detail="unique constraint on index failed")

        except:
            self.db.rollback()
            print("{}".format(sys.exc_info()))  

    async def delete(self, id):
        try:
            item = await self.read_by_id(id)
            if item:
                self.db.delete(item)
                self.db.commit()
            return True
        except:
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    
    async def filter_range(self, skip: int=0, limit: int=100, search:str = None, lower_boundary: float=0, upper_boundary:float=0):
        try:
            base = self.db.query(self.model)
            if lower_boundary and upper_boundary:
                try: 
                    base = base.filter(and_(
                        self.model.__table__.c[search] <= upper_boundary,
                        self.model.__table__.c[search] >= lower_boundary
                    ))
                except KeyError:
                    return base.offset(skip).limit(limit).all()
            return base.offset(skip).limit(limit).all()
        except:
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

    async def create(self, payload):
        try:  
            item = self.model(**payload.dict())
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item) 
            return item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="" )
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )                                        