from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: Optional[str]
    
class UserCreate(UserBase):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    image_url: Optional[str]
    is_verified: bool
    auth_type_id: int

class UserUpdate(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool]

class User(UserBase):
    pass

class UserSummary(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    is_verified: Optional[bool]

    class Config:
        orm_mode = True

class ResetPassword(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# # Properties to return to client
class RevokedToken(BaseModel):
    jti: str 
    # pass