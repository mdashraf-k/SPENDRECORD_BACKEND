from pydantic import BaseModel, Field
from datetime import datetime
 
class GroupsCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(max_length=200)


class GroupsOut(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True