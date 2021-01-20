from ..delivery_router.schemas import Delivery, DeliveryAddress, CreateDeliveryAddress, CreateDelivery
from ..product_router.schemas import Product
from ..payment_router.schemas import Payment
from typing import Optional, List
from pydantic import BaseModel, validator
import datetime

class OrderStateBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class CreateOrderState(OrderStateBase):
    pass

class UpdateOrderState(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]

class OrderState(OrderStateBase):
    id:int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

# ////////////////////

class CreateOrderItem(BaseModel):
    product_id: int
    quantity: int
    purchase_type_id: int
    duration: Optional[int]
   
    class Config:
        orm_mode=True

    @validator('quantity')
    def validate_quantity(cls, quantity):
        if quantity <= 0:
            raise ValueError('quantity cannot be less than 0')
        return quantity

    @validator('product_id')
    def validate_product_id(cls, product_id):
        if product_id <= 0:
            raise ValueError('product_id cannot be less than 0')
        return product_id

    

# //////////////////////

class OrderBillBase(BaseModel):
    total: float
    status: Optional[bool]

class CreateOrderBill(OrderBillBase):
    order_id: int
    payment_id: int

class UpdateOrderBill(BaseModel):
    order_id: Optional[int]
    payment_id: Optional[int]

class OrderBill(OrderBillBase):
    id: int
    payment: Payment 
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class OrderBase(BaseModel):
    status: Optional[bool]

class CreateOrder(OrderBase):
    owner_id: int
    voucher_id: Optional[int]
    
    delivery_price: float
    delivery_option_id: int
    order_items: List[CreateOrderItem]
    delivery: CreateDelivery
    

    # CreateOrder->{ 
    # owner_id
    # status
    # order_delivery ->{

    # }
    # order_items->[]:{
        # product_id
        # quantity
        # purchase_type_id
        # duration
    # }
    # }
    
class UpdateOrder(BaseModel):
    order_state_id: Optional[int]

class Order(OrderBase):
    id: int
    code: str
    owner_id: int
    order_state: OrderState
    order_bill: OrderBill
    order_delivery: Delivery
    order_items: List[Product]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

# product_weight: float
# product_weight_unit_id: int
# sub_total: Optional[int]
# order_bill: OrderBill
# Tax