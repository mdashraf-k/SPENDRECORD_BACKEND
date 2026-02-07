from pydantic import BaseModel, Field
from datetime import datetime
 
class GroupsCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class GroupsOut(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True