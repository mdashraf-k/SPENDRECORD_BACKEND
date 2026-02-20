from pydantic import BaseModel, Field
from datetime import datetime
from schemas.users import UsersOut

class SpendsCreate(BaseModel):
    description: str = Field(max_length=150)
    amount: int = Field(gt=0)


class SpendsOut(BaseModel):
    id: int
    amount: int
    description: str
    user: UsersOut
    created_at: datetime
    group_id: int

    class Config:
        from_attributes = True
