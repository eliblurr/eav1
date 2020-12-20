from ..weight_unit_router.schemas import WeightUnit
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
from ..reviews_router.schemas import Reviews
from typing import List, Optional
from pydantic import BaseModel
import datetime

class ImageBase(BaseModel):
    image_url: str
    product_id: int

class Image(ImageBase):
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
    purchase_type_id: int
    weight: Optional[float]
     
class CreateProduct(ProductBase):
    pass

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

class Product(ProductBase):
    id: int
    images: List[Image]
    reviews: List[Reviews]
    locations: List[Location]
    currency: Currency
    weight_unit: WeightUnit
    owner_id: int
    location_id: int
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True