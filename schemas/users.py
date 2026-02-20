from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsersCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=5, max_length=250)
    username: str = Field(min_length=5, max_length=50)
    password: str


class UsersOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True

class UserDetailsUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None, min_length=5, max_length=250)
    username: Optional[str] = Field(default=None, min_length=5, max_length=50)

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

