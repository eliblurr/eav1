from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserInfo(BaseModel):
    id: int
    user_id: int
    last_name: str
    first_name: str
    phone: Optional[str]
    status: Optional[bool]
    image_url: Optional[str]
    middle_name: Optional[str]
    is_verified: Optional[bool]
    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    
class CreateUser(UserBase):
    password: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    phone: Optional[str]
    image_url: Optional[str]
    is_verified: bool
    auth_type_id: int
    user_type_id: int
    status: Optional[bool]

class UpdateUser(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool]
    phone: Optional[str]
    status: Optional[bool]

class User(UserBase):
    id: int
    user_info: UserInfo
    
    class Config:
        orm_mode = True

class ResetPassword(BaseModel):
    password: str
    code: Optional[str]