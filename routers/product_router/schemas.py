from ..purchase_type_router.schemas import PurchaseType
from ..weight_unit_router.schemas import WeightUnit
from ..location_router.schemas import Location
from ..currency_router.schemas import Currency
from ..reviews_router.schemas import Review
from pydantic import BaseModel, conint, Field, validator
from typing import List, Optional
from fastapi import Form
import datetime, utils

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
    # weight_unit_id: Optional[conint(gt=0)]
    # wholesale_price: Optional[conint(gt=0)]
    # wholesale_quantity: Optional[conint(gt=0)]
    
class CreateProduct(ProductBase):
    country_id: conint(gt=0)
    category_ids: List[conint(gt=0)]
    event_ids: List[conint(gt=0)]
    location_ids: List[conint(gt=0)]
    payment_info: CreateProductPaymentInfo

    @validator('available_quantity')
    def assign_quantity(cls, v, values):
        if 'initial_quantity' in values and v > values['initial_quantity']:
            v = values['initial_quantity']
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
        batch_size:conint(gt=0)=Form(...),
        batch_price:float=Form(...),
        purchase_type_id:conint(gt=0)=Form(...),
        event_ids:List[str]=Form(...),
        category_ids:List[str]=Form(...),
        location_ids:List[str]=Form(...),
        available_quantity:Optional[conint(gt=0)]=Form(None),
        duration:Optional[conint(gt=0)]=Form(None)
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
        'CDF': Currency.CDF, 'CHE': Currency.CHE, 'CHF': Currency.CHF, 'CHW': Currency.CHW, 'CLF': Currency.CLF,
        'CLP': Currency.CLP, 'CNY': Currency.CNY, 'COP': Currency.COP, 'COU': Currency.COU, 'CAD': Currency.CAD,
        'CRC': Currency.CRC, 'CUC': Currency.CUC, 'CUP': Currency.CUP, 'CVE': Currency.CVE, 'CZK': Currency.CZK,
        'DJF': Currency.DJF, 'DKK': Currency.DKK, 'DOP': Currency.DOP, 'DZD': Currency.DZD, 'EGP': Currency.EGP,
        'ERN': Currency.ERN, 'ETB': Currency.ETB, 'EUR': Currency.EUR, 'FJD': Currency.FJD, 'FKP': Currency.FKP,
        'GBP': Currency.GBP, 'GEL': Currency.GEL, 'GHS': Currency.GHS, 'GIP': Currency.GIP, 'GMD': Currency.GMD,
        'GNF': Currency.GNF, 'GTQ': Currency.GTQ, 'GYD': Currency.GYD, 'HKD': Currency.HKD, 'HNL': Currency.HNL,
        'HRK': Currency.HRK, 'HTG': Currency.HTG, 'HUF': Currency.HUF, 'IDR': Currency.IDR, 'ILS': Currency.ILS,
        'INR': Currency.INR, 'IQD': Currency.IQD, 'IRR': Currency.IRR, 'ISK': Currency.ISK, 'JMD': Currency.JMD,
        'JOD': Currency.JOD, 'JPY': Currency.JPY, 'KES': Currency.KES, 'KGS': Currency.KGS, 'KHR': Currency.KHR,
        'KMF': Currency.KMF, 'KPW': Currency.KPW, 'KRW': Currency.KRW, 'KWD': Currency.KWD, 'KYD': Currency.KYD,
        'KZT': Currency.KZT, 'LAK': Currency.LAK, 'LBP': Currency.LBP, 'LKR': Currency.LKR, 'LRD': Currency.LRD,
        'LTL': Currency.LTL, 'LVL': Currency.LVL, 'LYD': Currency.LYD, 'MAD': Currency.MAD, 'MDL': Currency.MDL,
        'MGA': Currency.MGA, 'MKD': Currency.MKD, 'MMK': Currency.MMK, 'MNT': Currency.MNT, 'LSL': Currency.LSL,
        'MOP': Currency.MOP, 'MRO': Currency.MRO, 'MUR': Currency.MUR, 'MVR': Currency.MVR, 'MWK': Currency.MWK,
        'MXN': Currency.MXN, 'MXV': Currency.MXV, 'MYR': Currency.MYR, 'MZN': Currency.MZN, 'NAD': Currency.NAD,
        'NGN': Currency.NGN, 'NIO': Currency.NIO, 'NOK': Currency.NOK, 'NPR': Currency.NPR, 'NZD': Currency.NZD,
        'OMR': Currency.OMR, 'PAB': Currency.PAB, 'PEN': Currency.PEN, 'PGK': Currency.PGK, 'PHP': Currency.PHP,
        'PKR': Currency.PKR, 'PLN': Currency.PLN, 'PYG': Currency.PYG, 'QAR': Currency.QAR, 'RON': Currency.RON,
        'RSD': Currency.RSD, 'RUB': Currency.RUB, 'RWF': Currency.RWF, 'SAR': Currency.SAR, 'SBD': Currency.SBD,
        'SCR': Currency.SCR, 'SDG': Currency.SDG, 'SEK': Currency.SEK, 'SGD': Currency.SGD, 'SHP': Currency.SHP,
        'SLL': Currency.SLL, 'SOS': Currency.SOS, 'SRD': Currency.SRD, 'SSP': Currency.SSP, 'STD': Currency.STD,
        'SVC': Currency.SVC, 'SYP': Currency.SYP, 'SZL': Currency.SZL, 'THB': Currency.THB, 'TJS': Currency.TJS,
        'TMT': Currency.TMT, 'TND': Currency.TND, 'TOP': Currency.TOP, 'TRY': Currency.TRY, 'TTD': Currency.TTD,
        'TWD': Currency.TWD, 'TZS': Currency.TZS, 'UAH': Currency.UAH, 'UGX': Currency.UGX, 'USD': Currency.USD,
        'USN': Currency.USN, 'USS': Currency.USS, 'UYI': Currency.UYI, 'UYU': Currency.UYU, 'UZS': Currency.UZS,
        'VEF': Currency.VEF, 'VND': Currency.VND, 'VUV': Currency.VUV, 'WST': Currency.WST, 'XAF': Currency.XAF,
        'XAG': Currency.XAG, 'XAU': Currency.XAU, 'XBA': Currency.XBA, 'XBB': Currency.XBB, 'XBC': Currency.XBC,
        'XBD': Currency.XBD, 'XCD': Currency.XCD, 'XDR': Currency.XDR, 'XFU': Currency.XFU, 'XOF': Currency.XOF,
        'XPD': Currency.XPD, 'XPF': Currency.XPF, 'XPT': Currency.XPT, 'XSU': Currency.XSU, 'XTS': Currency.XTS,
        'XUA': Currency.XUA, 'YER': Currency.YER, 'ZAR': Currency.ZAR, 'ZMW': Currency.ZMW, 'ZWL': Currency.ZWL,
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