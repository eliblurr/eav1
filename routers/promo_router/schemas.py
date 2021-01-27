from pydantic import BaseModel
from typing import Optional
import datetime

class PromoVoucherBase(BaseModel):
    title: str
    metatitle: Optional[str]
    description: Optional[str]
    allowed_coverage: float
    discount: float
    status: bool

class CreatePromoVoucher(PromoVoucherBase):
    pass

class UpdatePromoVoucher(BaseModel):
    title: Optional[str]
    metatitle: Optional[str]
    description: Optional[str]
    status: Optional[bool]
    allowed_coverage: Optional[float]

class PromoVoucher(PromoVoucherBase):
    id: int
    promo_code: str
    user_id: Optional[int]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True