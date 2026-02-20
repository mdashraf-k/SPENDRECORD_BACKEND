from pydantic import BaseModel, Field
from datetime import datetime
from schemas.users import UsersOut


class GroupMemberAdd(BaseModel):
    user_id: int
    role: str = Field(min_length=3, max_length=20)

class GroupMemberUpdate(BaseModel):
    role: str | None = None
    is_active: bool | None = None


class GroupMemberOut(BaseModel):
    user: UsersOut
    role: str
    is_active: bool
    group_id: int
    joined_at: datetime

    class Config:
        from_attributes = True

