from sqlalchemy.orm import Session
from models.users import User


def add_user(db: Session, name:str, email: str, username: str, password_hash: str):
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