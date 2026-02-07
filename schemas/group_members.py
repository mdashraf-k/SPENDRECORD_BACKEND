from pydantic import BaseModel, Field
from datetime import datetime


class GroupMemberAdd(BaseModel):
    user_id: int
    role: str = Field(min_length=3, max_length=20)

class GroupMemberUpdate(BaseModel):
    role: str | None = None
    is_active: bool | None = None


class GroupMemberOut(BaseModel):
    user_id: int
    role: str
    is_active: bool
    group_id: int

    class Config:
        orm_mode = True

