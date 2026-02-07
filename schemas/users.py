from pydantic import BaseModel, EmailStr, Field

class UsersCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=250)
    username: str = Field(min_length=5, max_length=50)
    password: str


class UsersOut(BaseModel):
    id: int
    name: EmailStr
    email: str
    username: str

    class Config:
        orm_mode = True
