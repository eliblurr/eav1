from ..weight_unit_router.schemas import WeightUnit
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
from ..reviews_router.schemas import Reviews
from typing import List, Optional
from pydantic import BaseModel
from fastapi import Form
import datetime

class ProductImageBase(BaseModel):
    image_url: str
    product_id: int
    folder_name: Optional[str]

class CreateProductImage(ProductImageBase):
    pass

class UpdateProductImage(BaseModel):
    image_url: Optional[str]
    category_id: Optional[int]
    folder_name: Optional[str]

class ProductImage(ProductImageBase):
    id: int

    class Config:
        orm_mode=True

class ProductBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    unit_price: float
    serial_number: Optional[str]
    available_quantity: Optional[int]
    initial_quantity: int
    wholesale_price: Optional[float]
    wholesale_quantity: Optional[int]
    status: Optional[bool]
    weight: Optional[float]
    purchase_type_id: int
    weight_unit_id: Optional[int]
    owner_id: int
    currency_id: int
    
class CreateProduct(ProductBase):

    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(None), unit_price: float = Form(...), serial_number: str = Form(None), available_quantity: int = Form(None), initial_quantity:int = Form(...), wholesale_price:float=Form(None), wholesale_quantity:int=Form(...), status:bool=Form(True), weight:float=Form(None), purchase_type_id:int=Form(...), weight_unit_id:int=Form(None), owner_id:int=Form(...), currency_id:int=Form(...) ):
        return cls(title=title, metatitle=metatitle, description=description, unit_price=unit_price, serial_number=serial_number, available_quantity=available_quantity, initial_quantity=initial_quantity, wholesale_price=wholesale_price, wholesale_quantity=wholesale_quantity, status=status, weight=weight, purchase_type_id=purchase_type_id, weight_unit_id=weight_unit_id, owner_id=owner_id, currency_id=currency_id)

class UpdateProduct(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    unit_price: Optional[float]
    serial_number: Optional[str]
    available_quantity: Optional[int]
    initial_quantity: Optional[int]
    wholesale_price: Optional[float]
    wholesale_quantity: Optional[int]
    status: Optional[bool]
    purchase_type_id: Optional[int]
    weight: Optional[float]
    purchase_type_id: Optional[int]
    weight_unit_id: Optional[int]
    owner_id: Optional[int]
    currency_id: Optional[int]

class Product(ProductBase):
    id: int
    images: List[ProductImage]
    locations: List[Location]
    weight_unit: WeightUnit
    currency: Currency
    owner_id: int
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True