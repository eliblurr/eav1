from ..purchase_type_router.schemas import PurchaseType
from ..weight_unit_router.schemas import WeightUnit
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
from ..reviews_router.schemas import Review
from pydantic import BaseModel, conint, Field, validator
from typing import List, Optional
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
    purchase_type_id: int
    
class UpdateProductPaymentInfo(BaseModel):
    batch_price: Optional[float]
    batch_size: Optional[conint(gt=0)]
    duration: Optional[conint(gt=0)]
    purchase_type_id: Optional[int]

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
    available_quantity: Optional[int]
    initial_quantity: int
    wholesale_price: Optional[float]
    wholesale_quantity: Optional[int]
    status: Optional[bool]
    weight: Optional[float]
    weight_unit_id: Optional[conint(gt=0)]
    owner_id: conint(gt=0)
    
class CreateProduct(ProductBase):
    category_ids: List[int]
    event_ids: List[int]
    location_ids: List[int]
    payment_info: CreateProductPaymentInfo

    @classmethod
    def as_form(cls, title: str = Form(...), metatitle: str = Form(None), description: str = Form(...), unit_price: float = Form(...), serial_number: str = Form(None), available_quantity: int = Form(None), initial_quantity:int = Form(...), wholesale_price:float=Form(None), wholesale_quantity:int=Form(None), status:bool=Form(True), weight:float=Form(None), purchase_type_id:int=Form(...), weight_unit_id:int=Form(None), owner_id:int=Form(...), currency_id:int=Form(...), category_ids: List[int] = Form(...), event_ids: List[int] = Form(...),location_ids: List[int] = Form(...) ):
        return cls(title=title, metatitle=metatitle, description=description, unit_price=unit_price, serial_number=serial_number, available_quantity=available_quantity, initial_quantity=initial_quantity, wholesale_price=wholesale_price, wholesale_quantity=wholesale_quantity, status=status, weight=weight, purchase_type_id=purchase_type_id, weight_unit_id=weight_unit_id, owner_id=owner_id, currency_id=currency_id, category_ids=category_ids, event_ids=event_ids, location_ids=location_ids)

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
    weight: Optional[float]
    purchase_type_id: Optional[int]
    weight_unit_id: Optional[int]
    currency_id: Optional[int]

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

from pydantic import validator 
from money.money import Money
from money.currency import Currency

def get_currency(code):
    switcher = {
        'ALL': Currency.ALL, 'AMD': Currency.AMD, 'ANG': Currency.ANG, 'AOA': Currency.AOA, 'ARS': Currency.ARS, 
        'AUD': Currency.AUD, 'AWG': Currency.AWG, 'AZN': Currency.AZN, 'BAM': Currency.BAM, 'BBD': Currency.BBD, 
        'BDT': Currency.BDT, 'BGN': Currency.BGN, 'BHD': Currency.BHD, 'BIF': Currency.BIF, 'BMD': Currency.BMD, 
        'BND': Currency.BND, 'BOB': Currency.BOB, 'BOV': Currency.BOV, 'BRL': Currency.BRL, 'BSD': Currency.BSD, 
        'BTN': Currency.BTN, 'BWP': Currency.BWP, 'BYN': Currency.BYN, 'BYR': Currency.BYR, 'BZD': Currency.BZD, 
        'CDF': Currency.GBP, 'CHE': Currency.GBP, 'CHF': Currency.GBP, 'CHW': Currency.GBP, 'CLF': Currency.GBP, 
        'CLP': Currency.GBP, 'CNY': Currency.GBP, 'COP': Currency.GBP, 'COU': Currency.GBP, 'CAD': Currency.GBP, 
        'CRC': Currency.GBP, 'CUC': Currency.GBP, 'CUP': Currency.GBP, 'CVE': Currency.GBP, 'CZK': Currency.GBP, 
        'DJF': Currency.GBP, 'DKK': Currency.GBP, 'DOP': Currency.GBP, 'DZD': Currency.GBP, 'EGP': Currency.GBP, 
        'ERN': Currency.GBP, 'ETB': Currency.GBP, 'EUR': Currency.GBP, 'FJD': Currency.GBP, 'FKP': Currency.GBP, 
        'GBP': Currency.GBP, 'GEL': Currency.GBP, 'GHS': Currency.GBP, 'GIP': Currency.GBP, 'GMD': Currency.GBP, 
        'GNF': Currency.GBP, 'GTQ': Currency.GBP, 'GYD': Currency.GBP, 'HKD': Currency.GBP, 'HNL': Currency.GBP, 
        'HRK': Currency.GBP, 'HTG': Currency.GBP, 'HUF': Currency.GBP, 'IDR': Currency.GBP, 'ILS': Currency.GBP, 
        'INR': Currency.GBP, 'IQD': Currency.GBP, 'IRR': Currency.GBP, 'ISK': Currency.GBP, 'JMD': Currency.GBP, 
        'JOD': Currency.GBP, 'JPY': Currency.GBP, 'KES': Currency.GBP, 'KGS': Currency.GBP, 'KHR': Currency.GBP, 
        'KMF': Currency.GBP, 'KPW': Currency.GBP, 'KRW': Currency.GBP, 'KWD': Currency.GBP, 'KYD': Currency.GBP, 
        'KZT': Currency.GBP, 'LAK': Currency.GBP, 'LBP': Currency.GBP, 'LKR': Currency.GBP, 'LRD': Currency.GBP, 
        'LTL': Currency.GBP, 'LVL': Currency.GBP, 'LYD': Currency.GBP, 'MAD': Currency.GBP, 'MDL': Currency.GBP, 
        'MGA': Currency.GBP, 'MKD': Currency.GBP, 'MMK': Currency.GBP, 'MNT': Currency.GBP, 'LSL': Currency.GBP,
        'MOP': Currency.GBP, 'MRO': Currency.GBP, 'MUR': Currency.GBP, 'MVR': Currency.GBP, 'MWK': Currency.GBP, 
        'MXN': Currency.GBP, 'MXV': Currency.GBP, 'MYR': Currency.GBP, 'MZN': Currency.GBP, 'NAD': Currency.GBP, 
        'NGN': Currency.GBP, 'NIO': Currency.GBP, 'NOK': Currency.GBP, 'NPR': Currency.GBP, 'NZD': Currency.GBP, 
        'OMR': Currency.GBP, 'PAB': Currency.GBP, 'PEN': Currency.GBP, 'PGK': Currency.GBP, 'PHP': Currency.GBP, 
        'PKR': Currency.GBP, 'PLN': Currency.GBP, 'PYG': Currency.GBP, 'QAR': Currency.GBP, 'RON': Currency.GBP, 
        'RSD': Currency.GBP, 'RUB': Currency.GBP, 'RWF': Currency.GBP, 'SAR': Currency.GBP, 'SBD': Currency.GBP, 
        'SCR': Currency.GBP, 'SDG': Currency.GBP, 'SEK': Currency.GBP, 'SGD': Currency.GBP, 'SHP': Currency.GBP, 
        'SLL': Currency.GBP, 'SOS': Currency.GBP, 'SRD': Currency.GBP, 'SSP': Currency.GBP, 'STD': Currency.GBP, 
        'SVC': Currency.GBP, 'SYP': Currency.GBP, 'SZL': Currency.GBP, 'THB': Currency.GBP, 'TJS': Currency.GBP, 
        'TMT': Currency.GBP, 'TND': Currency.GBP, 'TOP': Currency.GBP, 'TRY': Currency.GBP, 'TTD': Currency.GBP, 
        'TWD': Currency.GBP, 'TZS': Currency.GBP, 'UAH': Currency.GBP, 'UGX': Currency.GBP, 'USD': Currency.GBP, 
        'USN': Currency.GBP, 'USS': Currency.GBP, 'UYI': Currency.GBP, 'UYU': Currency.GBP, 'UZS': Currency.GBP, 
        'VEF': Currency.GBP, 'VND': Currency.GBP, 'VUV': Currency.GBP, 'WST': Currency.GBP, 'XAF': Currency.GBP, 
        'XAG': Currency.GBP, 'XAU': Currency.GBP, 'XBA': Currency.GBP, 'XBB': Currency.GBP, 'XBC': Currency.GBP, 
        'XBD': Currency.GBP, 'XCD': Currency.GBP, 'XDR': Currency.GBP, 'XFU': Currency.GBP, 'XOF': Currency.GBP, 
        'XPD': Currency.GBP, 'XPF': Currency.GBP, 'XPT': Currency.GBP, 'XSU': Currency.GBP, 'XTS': Currency.GBP, 
        'XUA': Currency.GBP, 'YER': Currency.GBP, 'ZAR': Currency.GBP, 'ZMW': Currency.GBP, 'ZWL': Currency.GBP,
        'AED': Currency.AED, 'AFN': Currency.AFN
    }
    return switcher.get(code)

cc = lambda code : get_currency(code)

class A(BaseModel):
    code: str
    a:int

    @validator('a')
    def duration_validation(cls, value, values):
        if value and values['code']:
            return Money(value, cc(values['code'])).format('en_US')
        return value