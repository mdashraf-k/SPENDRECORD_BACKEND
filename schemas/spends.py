from pydantic import BaseModel, Field
from datetime import datetime

class SpendsCreate(BaseModel):
    description: str = Field(max_length=150)
    amount: int = Field(gt=0)


class SpendsOut(BaseModel):
    id: int
    amount: int
    description: str
    user_id: int
    created_at: datetime
    group_id: int

    class Config:
        orm_mode = True
