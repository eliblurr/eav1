from ..purchase_type_router.schemas import PurchaseType
from ..weight_unit_router.schemas import WeightUnit
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
from ..reviews_router.schemas import Review
from pydantic import BaseModel, conint, Field, validator
from typing import List, Optional
from fastapi import Form
import datetime, utils, collections
from money.money import Money

cc = lambda code : utils.get_currency(code)

class ProductImageBase(BaseModel):
    image_url: str
    product_id: int
    folder_name: Optional[str]

class CreateProductImage(ProductImageBase):
    pass

class UpdateProductImage(BaseModel):
    image_url: Optional[str]
    product_id: Optional[int]
    folder_name: Optional[str]

class ProductImage(ProductImageBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class ProductReview(BaseModel):
    reviews: List[Review]

    class Config:
        orm_mode = True

# ///////////////

class ProductPaymentInfoBase(BaseModel):
    batch_price: float
    batch_size: conint(gt=0)

class CreateProductPaymentInfo(ProductPaymentInfoBase):
    duration: Optional[conint(gt=0)]
    purchase_type_id: conint(gt=0)
    
class UpdateProductPaymentInfo(BaseModel):
    id:conint(gt=0)
    batch_price: Optional[float]
    batch_size: Optional[conint(gt=0)]
    duration: Optional[conint(gt=0)]
    purchase_type_id: Optional[conint(gt=0)]

class ProductPaymentInfo(ProductPaymentInfoBase):
    id: int
    currency: Currency
    purchase_type: PurchaseType
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode=True

class ProductBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: str
    serial_number: Optional[str]
    initial_quantity: conint(gt=0)
    available_quantity: Optional[conint(gt=0)]
    status: Optional[bool]
    weight: Optional[float]
    owner_id: conint(gt=0)
    
class CreateProduct(ProductBase):
    country_id: conint(gt=0)
    category_ids: List[conint(gt=0)]
    event_ids: List[conint(gt=0)]
    location_ids: List[conint(gt=0)]
    # payment_info: CreateProductPaymentInfo
    payment_info: List[CreateProductPaymentInfo]

    @validator('available_quantity')
    def assign_quantity(cls, v, values):
        if 'initial_quantity' in values and v > values['initial_quantity']:
            v = values['initial_quantity']
        return v
    
    @validator('payment_info')
    def unique_purchase_type(cls, v, values):
        _hldr= []
        for item in v:
            _hldr.append(item.purchase_type_id)
        if len([item for item, count in collections.Counter(_hldr).items() if count > 1]):
            raise ValueError('purchase type should be one of each')
        return v
    
    @classmethod
    async def as_form(
        cls,
        title:str=Form(...),
        metatitle:str=Form(None),
        description:str=Form(...),
        serial_number:str=Form(None),
        owner_id:conint(gt=0)=Form(...),
        initial_quantity:conint(gt=0)=Form(...),
        status:bool=Form(True),
        country_id:conint(gt=0)=Form(...),
        weight:Optional[float]=Form(None),
        event_ids:List[str]=Form(...),
        category_ids:List[str]=Form(...),
        location_ids:List[str]=Form(...),
        available_quantity:Optional[conint(gt=0)]=Form(None),
        duration:Optional[conint(gt=0)]=Form(None),
        batch_size:conint(gt=0)=Form(...),
        batch_price:float=Form(...),
        purchase_type_id:conint(gt=0)=Form(...)
    ):
        location_ids = await utils.string_list_to_int_list(location_ids[0].split(","))
        event_ids = await utils.string_list_to_int_list(event_ids[0].split(","))
        category_ids = await utils.string_list_to_int_list(category_ids[0].split(","))
        payment_info = { 'batch_price':batch_price, 'batch_size':batch_size, 'duration':duration, 'purchase_type_id':purchase_type_id }
        if available_quantity is None or available_quantity>initial_quantity:
            available_quantity=initial_quantity
        return cls(
            title=title,
            metatitle=metatitle,
            description=description,
            serial_number=serial_number,
            owner_id=owner_id,
            initial_quantity=initial_quantity,
            status=status,
            country_id=country_id,
            weight=weight,
            event_ids=event_ids,
            category_ids=category_ids,
            location_ids=location_ids,
            payment_info=payment_info,
            available_quantity=available_quantity
        )

class UpdateProduct(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    serial_number: Optional[str]
    initial_quantity: Optional[conint(gt=0)]
    available_quantity: Optional[conint(gt=0)]
    status: Optional[bool]
    weight: Optional[float]
    # owner_id: Optional[conint(gt=0)]
    # country_id: Optional[conint(gt=0)]
    payment_info: Optional[UpdateProductPaymentInfo]

class Product(ProductBase):
    id: int
    images: List[ProductImage]
    weight_unit: Optional[WeightUnit]
    currency: Currency
    owner_id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class A(BaseModel):
    code: str
    a:int

    @validator('a')
    def duration_validation(cls, value, values):
        if value and values['code']:
            return Money(value, cc(values['code'])).format('en_US')
        return value

from fastapi import Depends

class B(BaseModel):
    code: str
    a:int

    @classmethod
    def as_form(
        cls,
        code:str=Form(...),
        a:int=Form(...),
    ):
        return cls(
            code=code,
            a=a
        )

class C(BaseModel):
    jj:str
    ll: str
    B:B
    # D:Optional[List[B]]

    @classmethod
    def as_form(
        cls,
        k:int=Form(None),
        # jj:str=Form(...),
        # ll:str=Form(...),
        # kkk:str=Form(None),
        # G=Depends(B.as_form),
        B:List[B]=Form(...)
        # B=Depends(B.as_form),
    ):
        print(dir(B))
        print(B.json)
        return
        #  cls(
        #     jj=jj,
        #     ll=ll,
        #     # B=B
        # )

class K(BaseModel):
    pass

    @classmethod
    def as_form(
        cls,
        jj:B=Form(...),

    ):
        return