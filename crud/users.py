from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.users import User
from fastapi import HTTPException


def add_user(db: Session, name:str, email: str, username: str, password_hash: str):
    existing_users = db.query(User).filter(
        or_(User.email == email,
        User.username == username)
    ).all()

    errors = {}

    for existing in existing_users:
        if existing .email == email:
            errors["email"] = "Email already exists"
        if existing .username == username:
            errors["username"] = "Username already exists"
    
    if errors:
        raise HTTPException(
            status_code=400,
            detail=errors
        )
    user = User(
        name = name,
        email = email,
        username = username,
        password_hash = password_hash
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_info(db: Session, user):
    # db.query(User).filter(User.id == user.id).first()
    user_data = db.query(User).filter(User.id == user.id).first()
    if not user_data:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user_data
    # dict_user_data = {
    #     "id": user_data.id,
    #     "name": user_data.name,
    #     "username": user_data.username,
    #     "email": user_data.email,
    #     "created_date_time": user_data.created_at
    # }
    # return dict_user_data


def update_user_info(
        db: Session, 
        user_id: int, 
        name: str | None = None, 
        email: str | None = None,
        username: str | None = None
        ):
    
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if username is not None:
        user.username = username

    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user_id: int, new_password_hash:str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None
    
    user.password_hash = new_password_hash
    db.commit()
    db.refresh(user)
    return user