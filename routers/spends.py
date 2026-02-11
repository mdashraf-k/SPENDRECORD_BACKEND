from fastapi import APIRouter, status, HTTPException
from dependencies import DB, current_user
from schemas.spends import SpendsCreate
from crud.spends import add_spend, get_spends
from crud.helping_crud import is_group_member

router = APIRouter(
    prefix="/spend",
    tags=["Spends"]
)



@router.get("/{group_id}", status_code=status.HTTP_200_OK)
async def get_all_spends(db:DB, group_id:int, user:current_user):
    # Checking is the person group member
    # print(is_group_member(db=db, group_id=group_id, user_id=user.id))
    if not is_group_member(db=db, group_id=group_id, user_id=user.id):
        raise HTTPException(status_code=403, detail="You are not the member of this Group!")
    
    return get_spends(db=db, group_id=group_id)







@router.post("/{group_id}/spend", status_code=status.HTTP_200_OK)
async def create_spends(db: DB, group_id: int, spends: SpendsCreate, user: current_user):
   
   if not is_group_member(db=db, group_id=group_id, user_id=user.id):
       raise HTTPException(status_code=403, detail="You are not the member of this group!")
   
   return add_spend(db=db, description=spends.description, amount=spends.amount, user_id=user.id, group_id=group_id)