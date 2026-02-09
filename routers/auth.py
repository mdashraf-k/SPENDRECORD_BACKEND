from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from dependencies import get_db, password_hash
from schemas.users import UsersCreate
from crud.users import add_user
from sqlalchemy.orm import Session
from models.users import User
from sqlalchemy import or_
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from core.config import settings



router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)






class Token(BaseModel):
    access_token: str
    token_type: str

# class LoginRequest(BaseModel):
#     identifier: str   
#     password: str

db_dependency = Annotated[Session, Depends(get_db.get_db)]

def authenticate_user(identifier: str, password: str, db):
    user = db.query(User).filter(
        or_(
            User.username == identifier,
            User.email == identifier
            )
    ).first()

    if not user:
        return False
    if not password_hash.bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(days=settings.access_token_expire_days)
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)
    


    


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UsersCreate):
    
    hash_password = password_hash.bcrypt_context.hash(create_user_request.password)

    return add_user(
        db = db,
        name = create_user_request.name,
        email = create_user_request.email,
        username = create_user_request.username,
        password_hash = hash_password
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(identifier = form_data.username, password=form_data.password, db= db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    
    token = create_access_token(user.username, user.id)

    return {"access_token": token, "token_type": "bearer"}