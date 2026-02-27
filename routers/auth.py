from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from dependencies import db
from schemas.users import UsersCreate
from crud.users import add_user, user_exist_or_not
from sqlalchemy.orm import Session
from models.users import User
from sqlalchemy import or_
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from core.config import settings
from utils import security
from schemas.auth import LoginSchema
from google.oauth2 import id_token
from google.auth.transport import requests

expire = datetime.utcnow() + timedelta(days=30)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



class Token(BaseModel):
    access_token: str
    token_type: str

# class LoginRequest(BaseModel):
#     identifier: str   
#     password: str

db_dependency = Annotated[Session, Depends(db.get_db)]

def authenticate_user(identifier: str, password: str, db):
    user = db.query(User).filter(
        or_(
            User.username == identifier,
            User.email == identifier
            )
    ).first()

    if not user:
        return False
    if not security.bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(days=settings.access_token_expire_days)
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


@router.post("/google", status_code=status.HTTP_200_OK)
async def verify_user_by_google(db: db_dependency, response: Response, google_token: dict):
    
    try:
        idInfo = id_token.verify_oauth2_token(google_token["token"], requests.Request(), settings.google_clientid)

        email = idInfo["email"]
        name = idInfo["name"]

    except ValueError as e:
        # print(e)
        raise HTTPException(status_code=401, detail="Invalid Google Token")

    user = user_exist_or_not(db=db,email=email)

    if not user:
        # Signup automatically
        user = add_user(
        db = db,
        name = name,
        email = email,
        username = email.split("@")[0],
        password_hash = "google_oauth"
        )
    
    token = create_access_token(user.username, user.id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # True in production
        samesite=None,
        max_age=60 * 60 * 24 * 30
    )

    return {"message": "Google Login successful"}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, response: Response, create_user_request: UsersCreate):
    
    hash_password = security.bcrypt_context.hash(create_user_request.password)

    user = add_user(
        db = db,
        name = create_user_request.name,
        email = create_user_request.email,
        username = create_user_request.username,
        password_hash = hash_password
    )

    token = create_access_token(user.username, user.id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # True in production
        samesite=None,
        max_age=60 * 60 * 24 * 30,
        expires=expire
    )

    return {"message": "Login successful"}


@router.post("/login")
async def login(data: LoginSchema, response: Response, db: db_dependency):
    user = authenticate_user(identifier = data.identifier, password=data.password, db= db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    
    token = create_access_token(user.username, user.id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=24 * 60 * 60 * 30
    )

    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    return {"message": "Logged out"}