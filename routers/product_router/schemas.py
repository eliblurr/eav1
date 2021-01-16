from ..purchase_type_router.schemas import PurchaseType
from ..weight_unit_router.schemas import WeightUnit
from pydantic import BaseModel, conint, validator
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
import datetime, utils, collections, ast, re, sys
from ..reviews_router.schemas import Review
from fastapi import Form, HTTPException
from typing import List, Optional
from money.money import Money
from constants import dict_rx

gen_amount = lambda code : utils.get_currency(code)

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
    payment_info_id:conint(gt=0) # payment_info_id
    batch_price: Optional[float]
    batch_size: Optional[conint(gt=0)]
    duration: Optional[conint(gt=0)]
    purchase_type_id: Optional[conint(gt=0)]

class ProductPaymentInfo(ProductPaymentInfoBase):
    id: Optional[int]
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
    payment_info: List[CreateProductPaymentInfo]

    @validator('available_quantity')
    def assign_quantity(cls, v, values):
        if 'initial_quantity' in values and v > values['initial_quantity']:
            v = values['initial_quantity']
        return v
    
    @validator('payment_info')
    def unique_purchase_type(cls, v): 
        test = (len(v), len({v['purchase_type_id']:v for v in [item.dict() for item in v]}.values()) == len(v))
        if not all(test):
            raise HTTPException(status_code=422, detail="{}".format('payment info cannot be empty' if not test[0] else 'unique constraint failed on purchase_type_id'))
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
        payment_info:List[str]=Form(...)
    ):
        location_ids = await utils.string_list_to_int_list(location_ids[0].split(","))
        event_ids = await utils.string_list_to_int_list(event_ids[0].split(","))
        category_ids = await utils.string_list_to_int_list(category_ids[0].split(","))
        if available_quantity is None or available_quantity>initial_quantity:
            available_quantity=initial_quantity
        holder = re.findall(dict_rx, payment_info[0])
        payment_info = []
        for item in holder:
            try:
                payment_info.append(CreateProductPaymentInfo(**ast.literal_eval(item)))
            except:
                pass
         
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
            available_quantity=available_quantity,
            payment_info=payment_info
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
    payment_info: Optional[UpdateProductPaymentInfo]

class Product(ProductBase):
    id: int
    images: List[ProductImage]
    weight_unit: Optional[WeightUnit]
    payment_info: List[ProductPaymentInfo]
    # , ProductPaymentInfo
    # currency: Currency
    # owner_id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True
    
    @validator('payment_info')
    def payment_info_validation(cls, value):
        for item in value:
            print(item.batch_price)
            print(item.currency.title)
            item.batch_price = Money(str(item.batch_price), gen_amount(item.currency.title)).format('en_US')
            # item.currency.title
            # 
    #     if value and values['code']:
    #         return Money(value, gen_amount(values['code'])).format('en_US')
        return value

# Test Cases
class A(BaseModel):
    code: str
    a:int

    @validator('a')
    def duration_validation(cls, value, values):
        if value and values['code']:
            return Money(value, gen_amount(values['code'])).format('en_US')
        return value

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
    V:List[B]

    @validator('V')
    def v(cls, v):
        test = (len(v), len({v['a']:v for v in [item.dict() for item in v]}.values()) == len(v))
        if not all(test):
            raise HTTPException(status_code=422, detail="{}".format('V cannot be null' if not test[0] else 'unique constraint failed on a'))
        return v

    @classmethod
    def as_form( cls, jj:str=Form(...), ll:str=Form(...), V:List[str]=Form(...) ):   
        holder = re.findall(dict_rx, V[0])
        V = []
        for item in holder:
            try:
                V.append(B(**ast.literal_eval(item)))
            except:
                pass
        print(sys)
        return cls(jj=jj, ll=ll, V=V)

# {'code':'test_string', 'a': 2} 
# {'duration':4, 'batch_size':1, 'batch_price':2.2, 'purchase_type_id':2}
# duration:Optional[conint(gt=0)]=Form(None),
# batch_size:conint(gt=0)=Form(...),
# batch_price:float=Form(...),
# purchase_type_id:conint(gt=0)=Form(...)
# o={v['purchase_type_id']:v for v in [item.dict() for item in v]}.values()
# @validator('V')
# def v(cls, v):
#     o={v['a']:v for v in [item.dict() for item in v]}.values()
#     test = (len(v), len(o) == len(v))
#     if not all(test):
#         raise HTTPException(status_code=422, detail="{}".format('V cannot be null' if not test[0] else 'unique constraint failed on a'))
#     return v
# /////////////
# _hldr= []
# for item in v:
#     _hldr.append(item.purchase_type_id)
# if len([item for item, count in collections.Counter(_hldr).items() if count > 1]):
#     raise ValueError('purchase type should be one of each')
# return v
# payment_info = { 'batch_price':batch_price, 'batch_size':batch_size, 'duration':duration, 'purchase_type_id':purchase_type_id }
# o={v['a']:v for v in [item.dict() for item in v]}.values()
# payment_info: CreateProductPaymentInfo
# if sys.version_info[:2]<(2,6):
#   sys.stderr.write("You need python 2.6 or later to run this script\n")
#   exit(1)
# assert sys.version_info >= (2, 5)
# print ("Hello World!");
# import sys
# print(sys.version)
# print(sys.version[:3])
# print(sys.version_info[:2])
# if sys.version_info[:2] == (2, 6):
#     print('v2')
# if sys.version_info[:2] == (3, 6):
#     print('v3')
# L=[
#     {'id':1,'name':'john', 'age':34},
#     {'id':1,'name':'john', 'age':34},
#     {'id':2,'name':'hanna', 'age':30},
# ]
# a={v['id']:v for v in L}.values()
# b=list({v['id']:v for v in L}.values())
# print(a)
# print(b)
# print(len(a))
# print(len(b))