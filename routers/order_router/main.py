from fastapi import APIRouter, Depends, HTTPException, status
from . import crud, schemas, models
from sqlalchemy.orm import Session
from services import payment
from typing import List
from main import get_db

router2 = APIRouter()

@router2.post("/", description="create order state", status_code=201, response_model=schemas.OrderState)
async def create_order_state(payload:schemas.CreateOrderState, db:Session=Depends(get_db)):
    return await crud.create_order_state(payload, db)

@router2.get("/", description="read order states", response_model=List[schemas.OrderState])
async def read_order_states(skip:int=0, limit:int=100, search:str=None, value:str=None, db: Session=Depends(get_db)):
    return await crud.read_order_states(skip, limit, search, value, db)

@router2.get("/{id}", description="read order state by id", response_model=schemas.OrderState)
async def read_order_state_by_id(id:int, db:Session=Depends(get_db)):
    order_state = await crud.read_order_state_by_id(id, db)
    if order_state is None:
        raise HTTPException(status_code=404)
    return order_state

@router2.patch("/{id}", description="update order state", response_model=schemas.OrderState, status_code=status.HTTP_202_ACCEPTED)
async def update_order_state(id:int, payload:schemas.UpdateOrderState, db:Session=Depends(get_db)):
    return await crud.update_order_state(id, payload, db)

@router2.delete("/{id}", description="delete order by id", status_code=status.HTTP_202_ACCEPTED)
async def delete_order_state(id:int, db:Session=Depends(get_db)):
    return await crud.delete_order_state(id, db)

router = APIRouter()

# , response_model=schemas.Order
@router.post("/")
async def create_order(payload: schemas.CreateOrder, preview:bool=False, db: Session = Depends(get_db)):
    return payload

# @router.get("/", response_model=List[schemas.Order])
# async def get_order(skip: int=0, limit: int=100, search:str = None, value:str = None, db: Session = Depends(get_db)):
#     return

# @router.get("/{id}", response_model=schemas.Order)
# async def get_order_by_id(id: int, db: Session = Depends(get_db)):
#     return

# @router.patch("/{id}", response_model=schemas.Order)
# async def update_order(id: int, payload: schemas.UpdateOrder, db: Session = Depends(get_db)):
#     return

# @router.delete("/{id}")
# async def delete_order():
#     # if not await crud.delete_payment(id, db):
#     #     raise HTTPException( status_code=500)
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)
#     return

# @router.get("/bill_preview")

# make order
# - validate user[get usertype from token]
# cancel orer
# delete order
# - validate user[get usertype for token and check if user owns the product[admins can disable products]]
# rent products
# - validate user -> [get usertype from token -> validate payment -> [check if product quantity is >=] -> [create order for user -> update product details -> create scheduled job for when rental expires]]
# update rental period
# - update scheduled job [job id -> Type_UserID_product_ID]
# buy products
# - validate user -> [get usertype from token -> validate payment -> [check if product quantity is >=] -> [create order for user -> update product details]]
# read product[search]
# read product by id
