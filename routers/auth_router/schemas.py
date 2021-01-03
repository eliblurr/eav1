from ..users_router.schemas import UserBase, User
from pydantic import BaseModel
from typing import Optional

class Email(UserBase):
    pass

class Auth(UserBase):
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]

