from pydantic import BaseModel

class CurrentUser(BaseModel):
    id: int
    username: str

class LoginSchema(BaseModel):
    identifier: str
    password: str