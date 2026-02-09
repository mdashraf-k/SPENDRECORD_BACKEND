from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from dependencies import get_db, get_current_user, password_hash
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import PasswordUpdate, UserDetailsUpdate
from crud.users import update_user_password, update_user_info, get_user_info


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

db_dependency = Annotated[Session, Depends(get_db.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user.get_current_user)]
bcrypt_context = password_hash.bcrypt_context


@router.get("/", status_code= status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    # print(user)
    if user is None:
        return HTTPException(status_code=402, detail="Authentication Failed")
    
    return get_user_info(db=db, user=user)



@router.put("/edit_info", status_code=status.HTTP_200_OK)
async def edit_user_info(user: user_dependency, db: db_dependency, new_user_info: UserDetailsUpdate):
    if user is None:
        raise HTTPException(status_code=401, detail="Sorry, We didn't get the User")
    
    # Calling crude function
    update_user_info(db=db, user_id=user.get("id"), name=new_user_info.name, email=new_user_info.email, username=new_user_info.username)
   


@router.put("/edit_password", status_code=status.HTTP_200_OK)
async def edit_password(user: user_dependency, db: db_dependency, user_verification: PasswordUpdate):
    if user is None:
        raise HTTPException(status_code=401, detail="Error while changing password")
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.old_password, user_model.password_hash):
        raise HTTPException(status_code=401, detail="Error while changing password")
    
    new_password_hash = bcrypt_context.hash(user_verification.new_password)

    # calling crud function
    # print(user_model.id, new_password_hash)
    update_user_password(db= db, user_id = user_model.id, new_password_hash= new_password_hash)
    


    