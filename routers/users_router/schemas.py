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

class UserUpdate(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool]
    phone: Optional[str]

class ResetPassword(BaseModel):
    password: Optional[str]

    class Config:
        orm_mode = True



class UserInfo(BaseModel):
    id: int
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    image_url: Optional[str]
    is_verified: bool

    date_created: datetime.datetime
    date_modified: datetime.datetime

    class Config:
        orm_mode = True

class User(UserBase):
    user_info : UserInfo
    
    class Config:
        orm_mode = True


# class Token(BaseModel):
#     access_token: str
#     token_type: str

#     class Config:
#         orm_mode = True

# # # Properties to return to client
# class RevokedToken(BaseModel):
#     jti: str 
#     # pass


# class UserSummary(BaseModel):
#     first_name: Optional[str]
#     middle_name: Optional[str]
#     last_name: Optional[str]
#     image_url: Optional[str]
#     is_verified: Optional[bool]

#     class Config:
#         orm_mode = True

# class ResetPassword(BaseModel):
#     password: str

#     class Config:
#         orm_mode = True