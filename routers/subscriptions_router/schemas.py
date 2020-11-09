from pydantic import BaseModel
from typing import Optional

import datetime

from ..priorities_router.schemas import Priority

class SubscriptionType(BaseModel):
    id: int
    title: str
    # metatitle: Optional[str]
    # description: Optional[str]

    class Config():
        orm_mode = True

# ///////////////////////////////////// #


class SubscriptionBase(BaseModel):
    title: str 
    metatitle: Optional[str]
    description: Optional[str]
    price: float
    duration: Optional[int]

class SubscriptionCreate(SubscriptionBase):
    priority_id: int
    subscription_type_id: int

class SubscriptionUpdate(BaseModel):
    title: Optional[str] 
    metatitle: Optional[str]
    description: Optional[str]
    price: Optional[float]
    duration: Optional[int]
    priority_id: Optional[int]
    subscription_type_id: Optional[int]

class Subscription(SubscriptionBase):
    id: int
    date_created: datetime.datetime
    date_modified: datetime.datetime
    priority: Priority
    subscription_type: SubscriptionType

    class Config():
        orm_mode = True


# {
#   "date_created": "2020-10-31T23:04:45.152873",
#   "priority_id": 1,
#   "price": 0,
#   "metatitle": "string",
#   "id": 3,
#   "date_modified": "2020-10-31T23:04:45.152880",
#   "subscription_type_id": 1,
#   "duration": 0,
#   "description": "string",
#   "title": "string"
# }