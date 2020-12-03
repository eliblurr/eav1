from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    phone: Optional[str]
    image_url: Optional[str]
    is_verified: bool
    auth_type_id: int
    status: Optional[bool] = True

class UserUpdate(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool]
    phone: Optional[str]
    status: Optional[bool]

class ResetPassword(BaseModel):
    password: str

class UserInfo(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool] = True
    status: Optional[bool] = True

    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    user_info : UserInfo
    
    class Config:
        orm_mode = True